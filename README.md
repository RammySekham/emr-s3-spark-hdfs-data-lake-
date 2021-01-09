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

