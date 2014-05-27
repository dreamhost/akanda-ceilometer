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


"""Test the ceilometer entrypoint for the notification collector
"""

import pkg_resources
import unittest

from akanda.ceilometer.notifications import NetworkBandwidthNotification


class TestCeilometerNotificationEntryPoint(unittest.TestCase):

    NAMESPACE = 'ceilometer.collector'

    def setUp(self):
        self.plugins = []
        for ep in pkg_resources.iter_entry_points(group=self.NAMESPACE):
            plugin = ep.load()
            self.plugins.append(plugin)

    def test_notification_entry_point(self):
        assert NetworkBandwidthNotification in self.plugins
