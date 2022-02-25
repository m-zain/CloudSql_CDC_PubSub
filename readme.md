**Copyright 2021 Google Inc.**  
**Licensed under the Apache License, Version 2.0 (the "License");**  
**you may not use this file except in compliance with the License.**  
**You may obtain a copy of the License at**  

**http://www.apache.org/licenses/LICENSE-2.0**  

**Unless required by applicable law or agreed to in writing, software**  
**distributed under the License is distributed on an "AS IS" BASIS,**  
**WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.**  
**Author: Muhammad Zain ul Islam, PSO Google.**  
**Your use of it is subject to your agreement with Google.**  
**Following open source material have been used while writing the code as well**  
**https://www.postgresqltutorial.com/postgresql-python/connect/**  
**https://www.psycopg.org/docs/advanced.html#replication-support**  

#Description and Instructions for running the code to deliver every change—insert, update, and delete  data from CloudSql Postgres into Pub/Sub.
**Currently the solution will be deployed on a VM in GCP and will be connected to Postgres by a replication slot and each change will be pubslished to Pub/sub**

**Programming Language:**  
Python 3.7+

**Steps to configure the Environment**

*Creating and configuring permissions for Virtual Machine* 
1) Create a new VM.  
   Follow the instructions here to create and start a new VM: https://cloud.google.com/compute/docs/instances/create-start-instance
2) While creating a VM, Under the `Identity and API access` section, chose the default `Compute Enginere default service account` and under `access scopes` select the option `Allow full access to Google cloud APIs`.
3) After creating the VM, go to the IAM & adming page, edit the VM's service account and Assign the service account the IAM permission `Pub/Sub Publisher` allowing to publish events to Pub/sub.

*Configuring the VM to install requirements to Use Python*
After the VM has been installed, SSH into the VM to install Pip, Python, 

1. Install and use Python virtual environment in the VM.
   Detailed steps can be found here: https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b

2. Install pip3 for python3.
   
   1) `sudo apt-get update`
   2) `sudo apt-get -y install python3-pip`
   3) `pip3 --version`
  
   Article with more details: https://www.educative.io/edpresso/installing-pip3-in-ubuntu

3. Install Postgres client  

    1. `sudo apt-get update`
    2. `sudo apt-get install postgresql-client`
    3. `gcloud sql connect replication-cdc  --user=postgres`  
       Postgres link with more details: https://wiki.postgresql.org/wiki/Apt
       
       
4. Install psycopg2:  
        `pip3 install psycopg2`  
        `Code` from here:https://www.postgresqltutorial.com/postgresql-python/connect/ 
   
5. Install Pub/sub 
   ```pip3 install --upgrade google-cloud-pubsub``` 
   
6. Give the Service account permission through IAM to be able to publish events to Pub/sub. Role required is `Pub/Sub Publisher`


**CloudSql-Postgres Instructions**
1. Postgres super user is required with the role replication. 
   
    https://cloud.google.com/sql/docs/postgres/replication/configure-logical-replication#examples 

2. Turn on the following database flags 
   1) `cloudsql.logical_decoding`
   2)  `cloudsql.enable_pglogical`.  
       Please follow the instructions here to see how to turn on database flags:
       https://cloud.google.com/sql/docs/postgres/flags#set_a_database_flag

Mode details around replication of CDC can be found here: 
       
https://cloud.google.com/sql/docs/postgres/replication/configure-logical-replication#receiving-decoded-wal-changes-for-change-data-capture

https://cloud.google.com/sql/docs/postgres/replication/configure-logical-replication#setting-up-logical-replication-with-pglogical



#Database.ini file
Add the values for Ip, db_name, user and password. 

#publish.py file
Replace the project_id and topic_id values with correct values to build the path.

#Useful information around CloudSQL CDC, logical replication. 
1. https://cloud.google.com/sql/docs/postgres/replication/configure-logical-replication
2. https://www.psycopg.org/docs/extras.html#replication-support-objects
#Filtering tables, schemas in Wal2Json.   
3. https://github.com/eulerto/wal2json#parameters
4. https://stackoverflow.com/questions/32407764/its-possible-to-use-logical-decoding-to-replicate-a-single-table


