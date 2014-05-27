# Copyright 2014 DreamHost, LLC
#
# Author: DreamHost, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from setuptools import setup, find_packages

setup(
    name='akanda-ceilometer',
    version='0.1.0',
    description='Ceilometer plugin for processing Akanda notifications',
    author='DreamHost',
    author_email='dev-community@dreamhost.com',
    url='http://github.com/dreamhost/akanda',
    license='BSD',
    install_requires=['ceilometer'],
    namespace_packages=['akanda'],
    packages=find_packages(exclude=['test', 'smoke']),
    entry_points={
        'ceilometer.collector': [
            'akanda_bandwidth = akanda.ceilometer.notifications'
            ':NetworkBandwidthNotification',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    )
