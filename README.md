### Introduction: 
##### As the startup business grows, so the data. Spariky-a music streaming app company has decided to maintain the Data Lake for all types of data considering benefits of Data Lake i.e. 'Schema on Road', 'storage of high to low value data'  and  'storage of any type and format of data'. 

##### ELT Processes: Data will be extracted from all the sources i.e. operational processes, loaded into Data Lake , transformed for analytics & BI reporting using Schema on Road.

#### What AWS offers:
##### To run data processing for lake, We have three options.
###### 1. EMR (HDFS + SPARK) - once data is ingested from different AWS data sources, all data stored on HDFS and processed on cluster through query in place. This cluster is not supposed to shut down, can grow as data grows.If shut down,  will involve loss of data stored after querying from HDFS storage unless data is transferred to S3 for permanent stroage.
###### 2. EMR (S3 + SPARK) - All data is stored in S3.Data is loaded from S3, queried and results are stored back to s3. The EMR- Cluster can spun on demnad , can be shut down if not needed for processing
###### 3. Serverless Anthena - All data is stored in s3. Athena can load, process data on serverless lambda resources. It is pay as you execute model, not pay for machine up time model.

### Project
##### For this project I run EMR with Hadoop and queried the data with Spark from S3 and stored on HDFS system and then transferred to S3 for permanent storage.

#### Configuration Settings for Spark Job on EMR:
##### What type of instances do I need?:
###### -EC2 instances: For memory intensive it is R type, for Compute intensive it is C type and for general purposes - M type.I selected M5 after reading use Cases for M5 on AWS. It is used for Small and mid-size databases, data processing tasks that require additional memory, caching fleets, and for running b  ackend servers for SAP, Microsoft SharePoint, cluster computing, and other enterprise applications
###### -Spot instances: This option offers up to 90% cost reduction when compared to on-demand pricing. I thought of deploying spot instances only for core and task nodes, not for master node considering their drawback of possible interruption in service.
##### How many instances do I need for core or task nodes?
###### -This should be done based on the size of the input datasets, application execution times, and frequency requirements.I have small datasets. I have certain operation such as join, group by which are memory intensive, have read from S3 and write operations to HDFS and from HDFS back to S3.I took guidance from:[Amazon EMR Best Practices](https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/).I followed these instructions: However, I have very small dataset, I have modified few things according to small dataset. Configurations can be found in config file in this repository.

### Project Flow

##### 1. Getting size of the S3 data:
          
          $ aws s3 ls --summarize --human-readable --recursive <bucket Name/folder> |grep "Total Size"

##### 2.  Getting the sample of data and preparing ELT processes. I have done in three parts:
         
         elt_prep_file : I have prepared all spark-jobs to process data in interative jupyter note book environment in spark local mode
         elt_local_test : I have created python script from elt_prep_file and tested the script on my local spark-shell
         elt_py: I have curated my elt_local_test file according to EMR cluster env. i.e. Updating s3 and hdfs links for reading and writing data
         
 ##### 3. We can create cluster by AWS cli or manually. I created manually to leverage spot instances option.
 ##### 4. Then connecting local system to master-node using SSH
     
         ssh -i pemfile hadoop@ec2-*******.us-west-2.compute.amazonaws.com
 ##### 5. Created Hadoop directory for output files , with same name what I have mentioned in my script to save output files
         
         hdfs dfs -mkdir \user\Data
 ##### 6. Copy Script to EMR Cluster
        
         scp -i pemfile elt.py masternode:~/
 ##### 7. Submitted Spark Script to cluster for run
      
        user/spark/bin spark-submit elt.py
 ##### 8. Copied output from HDFS to S3
         
         s3-dist-cp --src hdfs:///user/Data --dest s3://<bucket-name>/Data
  
 ##### Note, we can monitor the health of cluster using Spark Web UI, can be accessed by establishing SSH-tunnel for interfaces.[Link](https://medium.com/@mht.amul/running-sparkui-on-amazon-emr-4b7b5b8f64e)
  
  ##### The Final Output Snapshot:
  
  ![](https://github.com/RammySekham/lake-elt/blob/main/S3_output.PNG)
  






