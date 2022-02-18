# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# Your use of it is subject to your agreement with Google.


# Author: Muhammad Zain ul Islam, PSO Google.
# Following open source material have been used while writing the code as well
# https://www.postgresqltutorial.com/postgresql-python/connect/
# https://www.psycopg.org/docs/advanced.html#replication-support
#


from __future__ import print_function
import sys
import psycopg2
import psycopg2.extras
from config import config
from publish import publish_messages

class DemoConsumer(object):
    def __call__(self, msg):
       
        #print(msg.payload)
        
        # pushing msgs to pub/sub
        publish_messages(msg.payload)
        
        # Sending feedback to postgres about consumed msgs.
        msg.cursor.send_feedback(flush_lsn=msg.data_start)

def replication():
    """
    1) Connect to the PostgreSQL database server
    2) Create and start logical replication with Postgres Server.
    3) Call the Pub/sub function to push to Pub/Sub
    """

    conn = None
    try:
        # read connection parameters
        dsn = config()
        

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(dsn,
                connection_factory=psycopg2.extras.LogicalReplicationConnection)
	
        print('Connection created')
        # create a cursor
        cur = conn.cursor()
        # replication slot name
        replication_slot = 'postgres_replication'
        try:
            # Start replication slot if available
            cur.start_replication(slot_name=replication_slot, decode=True)
        except psycopg2.ProgrammingError:
            # Create replication slot only the first time, with wal2json decoding.
            cur.create_replication_slot(replication_slot, output_plugin='wal2json')
            cur.start_replication(slot_name=replication_slot, decode=True)

    
        print('calling streaming')
        democonsumer = DemoConsumer()
        print("Starting streaming, press Control-C to end...", file=sys.stderr)
        try:
            #consuming the stream msgs.
            cur.consume_stream(democonsumer)
        except KeyboardInterrupt:
            cur.close()
            conn.close()
            print("The slot " + replication_slot + "still exists. Drop it by running following command on Postgres:  "
                    "SELECT pg_drop_replication_slot('" + replication_slot + "'); if no longer needed.", file=sys.stderr)
            
            print("WARNING: Transaction logs will accumulate in pg_xlog "
                    "until the slot is dropped.", file=sys.stderr)
            
            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    replication()

