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
