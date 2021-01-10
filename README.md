### Introduction: 
##### As the startup business grows, so the data. Sparkify-a music streaming app company has decided to maintain the Data Lake for all types of data considering benefits of Data Lake i.e. 'Schema on Road', 'storage of high to low value data'  and  'storage of any type and format of data'. 
##### ELT Processes: Data will be extracted from all the sources i.e. operational processes, loaded into Data Lake, transformed for analytics & BI reporting using Schema on Road.
#### What AWS offers:
##### To run data processing for lake, there are three options.
###### 1. EMR (HDFS + SPARK) - Once data is ingested from different AWS data sources, all data is stored on HDFS and processed on cluster through query in place. This cluster is not supposed to shut down, can grow as data grows. If this cluster is shut down, it involves loss of data stored in HDFS storage after querying unless data is transferred to S3 for permanent storage.
###### 2. EMR (S3 + SPARK) - All the data is stored in S3. Data is loaded from S3, queried and results are stored back to S3. The EMR- Cluster can spun on demand, can be shut down if not needed for processing.
###### 3. Serverless Athena - All data is stored in S3. Athena can load, process data on serverless lambda resources. It is 'pay as you execute' model, not a 'pay for machine up time' model.

### Project
##### For this project, EMR with Hadoop is used and data is queried with Spark from S3 and stored on HDFS system and then transferred to S3 for permanent storage.
##### `Tools`: emr-5.32.0, Hadoop distribution: Amazon 2.10.1, Spark 2.4.7, Ganglia 3.7.2, EC2 instances: Mix of m4.large, m1.large, m5.large, Python lib: pyspark.sql
##### `Input Raw Data` : JSON logs on user activity on the app and JSON metadata on the songs in the app hosted on S3 Bucket
##### `Output Data`: A Fact table of Songs-Played and Dimenisons Tables: Users, Songs, Artists and time


#### Configuration Settings for Spark Job on EMR:
###### -EC2 instances: General purpose M types instances are considered as per use cases listed on AWS website
###### -Spot instances: This option offers up to 90% cost reduction when compared to on-demand pricing. Spot instances are deployed only for core and task nodes, not for master node considering their drawback of possible interruption in service.
###### -Steps are followed from: [Amazon EMR Best Practices](https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/) for configurations.
### Project Flow

##### 1. Getting size of the S3 data:
          
          $ aws s3 ls --summarize --human-readable --recursive <bucket Name/folder> |grep "Total Size"

##### 2. Getting the sample of data and preparing ELT processes. It is done in three parts:
         
         elt_prep_file : Preparation of all spark-jobs to process data in interactive Jupyter notebook in spark local mode
         elt_local_test : Created python script from elt_prep_file and testing of the script on local spark-shell
         elt_py: Curated elt_local_test file according to EMR cluster env. i.e. updating S3 and HDFS links for reading and writing data
         
 ##### 3. EMR Cluster can be created by AWS CLI or manually. Here, it is created manually to leverage spot instances option.
 ##### 4. Connection of local system to master-node using SSH
     
         ssh -i pemfile hadoop@ec2-*******.us-west-2.compute.amazonaws.com
 ##### 5. Creating Hadoop directory for output files, with same name what is mentioned in python script to save output files
         
         hdfs dfs -mkdir \user\Data
 ##### 6. Copying python script to EMR Cluster
        
         scp -i pemfile elt.py masternode:~/
 ##### 7. Submitting script to spark cluster for run
      
        user/spark/bin spark-submit elt.py
 ##### 8. Copying output from HDFS to S3
         
         s3-dist-cp --src hdfs:///user/Data --dest s3://<bucket-name>/Data
  
 ##### Note, we can monitor the health of cluster using Spark Web UI, can be accessed by establishing SSH-tunnel for interfaces. [Link](https://medium.com/@mht.amul/running-sparkui-on-amazon-emr-4b7b5b8f64e)
  
  ##### One of the output table after running spark-application on EMR:
  
  ![](https://github.com/RammySekham/lake-elt/blob/main/S3_output.PNG)
