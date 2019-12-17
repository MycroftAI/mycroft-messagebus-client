# Copyright (c) 2018 Mycroft AI, Inc.
#
# This file is part of Mycroft Skills Manager
# (see https://github.com/MatthewScholefield/mycroft-light).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from setuptools import setup


with open("README.md", "r") as fh:
    long_desc = fh.read()


setup(
    name='mycroft-messagebus-client',
    version='0.8.1',
    packages=['mycroft_bus_client', 'mycroft_bus_client.client',
              'mycroft_bus_client.util'],
    install_requires=['websocket-client==0.54.0',
                      'pyee==5.0.0'],
    url='https://github.com/MycroftAI/mycroft-messagebus',
    license='Apache-2.0',
    author='Mycroft AI, Åke Forslund',
    author_email='devs@mycroft.ai, ake.forslund@mycroft.ai',
    description='Mycroft Messagebus Client',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    data_files=[('mycroft_bus_client', ['LICENSE.md'])]
)
