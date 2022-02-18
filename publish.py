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


from google.cloud import pubsub_v1

# Enter project_id and topic_id values.
project_id = "Enter the project_id here"
topic_id = "Enter the topic_id here"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

def publish_messages(payload):
    data = payload
    # Data must be a bytestring
    data = data.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

