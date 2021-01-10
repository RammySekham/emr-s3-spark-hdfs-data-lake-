
# File to run on emr cluster

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql import Window


def create_spark_session():
    '''

    Function creates spark-session

    '''
    spark = SparkSession.builder.config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0").getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    
    '''                              
   
    Function process the input_data with spark and write processed data to disk
   
    '''

    # get filepath to song data file
    song_data = input_data +  "song_data/*/*/*/*.json"
    
    
    # read song data file
    df = spark.read.json(song_data, multiLine=True)
    

    # extract columns to create songs table
    songs_table = df.filter("song_id is NOT NULL")\
                   .select("song_id","title", "artist_id", "year", "duration").dropDuplicates()
  
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(output_data + "Data/songs", mode="overwrite", partitionBy=('year', 'artist_id'), compression='snappy')
    

    # extract columns to create artists table
    artists_table = df.alias("one").filter("artist_id is NOT NULL").groupby("artist_id").agg({'year':'max'})\
                      .join(df.alias("two"), (col("one.artist_id")==col("two.artist_id")) & ("max(year)"==col("two.year")), 'left')\
                      .select("one.artist_id", col("artist_location").alias("location"), col("artist_latitude").alias("latitude"),\
                       col("artist_longitude").alias("longitude")).distinct()
    
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + "Data/artists", mode="overwrite", compression='snappy')


def process_log_data(spark, input_data, output_data):
    
    '''
    Function process the log data with spark, write it to disk
    
    '''
    
   
    # get filepath to log data file
    log_data = input_data + "log_data/*.json"
    song_data = input_data + "song_data/*/*/*/*.json"
    

    # read log data file
    df = spark.read.json(log_data, multiLine=True)
    
    
    # filter by actions for song plays, where user id is not null
    dft = df.filter((col("page") =='NextSong')).dropDuplicates()
    
    dff = dft.filter(col("userId").isNotNull()).groupby('userId').agg({'ts':'max'}) 
    
    
    # extract columns for users table    
    user_table = df.join(dff, (df.ts=="max(ts)") & (df.userId==dff.userId), 'right')\
                   .select(df.userId.alias("user_id"),\
                     col("firstName").alias("first_name"),\
                     col("lastName").alias("last_name"), "gender", "level").distinct()
    
    
    # write users table to parquet files
    user_table.write.parquet(output_data + "Data/users", mode="overwrite", compression='snappy')

    
    # create timestamp column from original timestamp column
    df = df.select(from_unixtime(col("ts")/1000).alias("time_stamp"))
    
    
    # extract columns to create time table
    time_table = df.select(col("time_stamp").alias("start_time"), hour(col("time_stamp")).alias("hour"),\
                                  dayofmonth(col("time_stamp")).alias("day"), weekofyear(col("time_stamp")).alias("week"),\
                                  month(col("time_stamp")).alias("month"), year(col("time_stamp")).alias("year"),\
                                  dayofweek(col("time_stamp")).alias("weekday")).distinct()
    
    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(output_data + "Data/time", mode="overwrite", partitionBy=('year', 'month'), compression='snappy')

    # read in song data to use for songplays table
    dfs = spark.read.json(song_data, multiLine=True)

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = dft.join(dfs,(dft.artist==dfs.artist_name)\
                               & (dft.song==dfs.title), 'left')\
                               .select(from_unixtime(col("ts")/1000).alias("start_time"),\
                               month(from_unixtime(col("ts")/1000)).alias("month"),\
                               year(from_unixtime(col("ts")/1000)).alias("year"),\
                               col("userId").alias("user_id"), "level", dfs.song_id, dfs.artist_id,\
                               col("sessionId").alias("session_id"), "location", col("userAgent").alias("user_agent"))
    
    window= Window.orderBy("start_time")
    songplays_table = songplays_table.withColumn('songplay_id', row_number().over(window))

    # write songplays table to parquet files partitioned by year and month

    songplays_table.select("songplay_id", "start_time", "user_id", "level","session_id",\
                           "location", "user_agent", "year","month").write.parquet(output_data + "Data/songplays",\
                            mode="overwrite", partitionBy=('year', 'month'), compression='snappy')


def main():
    '''
    Calls data processing fucntions
    
    '''
    
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "hdfs:///user/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
