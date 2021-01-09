Introduction: As the startup business grows, so the data. Spariky-a music streaming app company has decided to maintain the Data Lake for all types of data considering benefits of Data Lake i.e. 'Schema on Road', 'storage of high to low value data'  and  'storage of any type and format of data'. 

ELT Processes:
Data will be extracted from all the sources i.e. operational processes, loaded into Data Lake , transformed for analytics & BI reporting y using Schema on Road

What AWS offers:
To run data processing for lake, We have three options.
1. EMR (HDFS + SPARK) - once data is ingested from different AWS data sources, all data stored on HDFS and processed on cluster through query in place. This cluster is not supposed to shut down, can grow as data grows. If shut down,  will involve loss of data from HDFS storage unless data is transferred to S3 for permanent stroage.
2. EMR (S3 + SPARK) -
