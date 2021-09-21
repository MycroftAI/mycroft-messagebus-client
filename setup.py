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
import os
from setuptools import setup


with open("README.md", "r") as fh:
    long_desc = fh.read()


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_dir, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name='mycroft-messagebus-client',
    version='0.9.3',
    packages=['mycroft_bus_client', 'mycroft_bus_client.client',
              'mycroft_bus_client.util'],
    package_data={
      '*': ['*.txt', '*.md']
    },
    include_package_data=True,
    install_requires=required('requirements.txt'),
    url='https://github.com/MycroftAI/mycroft-messagebus-client',
    license='Apache-2.0',
    author='Mycroft AI, Åke Forslund',
    author_email='devs@mycroft.ai, ake.forslund@gmail.com',
    description='Mycroft Messagebus Client',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
