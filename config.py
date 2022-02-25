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

from configparser import ConfigParser

# preparing dsn connection address

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    dsn = ""
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if not dsn:
                dsn = param[0] + "=" + param[1]
            else:
                dsn = dsn + " " + param[0] + "=" + param[1]
        
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return dsn
