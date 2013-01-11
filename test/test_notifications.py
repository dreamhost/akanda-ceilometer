import mock
import unittest

from akanda.ceilometer.notifications import NetworkBandwidthNotification
from ceilometer.openstack.common import cfg

BW_NOTIFICATION = {
    u'_context_auth_token': u'3d8b13de1b7d499587dfc69b77dc09c2',
    u'_context_is_admin': True,
    u'_context_project_id': u'7c150a59fe714e6f9263774af9688f0e',
    u'_context_quota_class': None,
    u'_context_read_deleted': u'no',
    u'_context_remote_address': u'10.0.2.15',
    u'_context_request_id': u'req-d68b36e0-9233-467f-9afb-d81435d64d66',
    u'_context_roles': [u'admin'],
    u'_context_timestamp': u'2012-05-08T20:23:41.425105',
    u'_context_user_id': u'1e3ce043029547f1a61c1996d1a531a2',
    u'event_type': u'akanda.bandwidth.used',
    u'message_id': u'dae6f69c-00e0-41c0-b371-41ec3b7f4451',
    u'payload': {u'external': {u'out.packets': 1234,
                               u'out.bytes': 22434,
                               u'in.packets': 88,
                               u'in.bytes': 89420,
                               },
                 u'internal': {u'out.packets': 4567,
                               u'out.bytes': 82984,
                               u'in.packets': 77,
                               u'in.bytes': 98982,
                               }
                 },
    u'priority': u'INFO',
    u'tenant_id': u'7c150a59fe714e6f9263774af9688f0e',
    u'timestamp': u'2012-05-08 20:23:48.028195',
    }

BW_NOTIFICATION_ALT = {
    u'_context_auth_token': u'3d8b13de1b7d499587dfc69b77dc09c2',
    u'_context_is_admin': True,
    u'_context_project_id': u'7c150a59fe714e6f9263774af9688f0e',
    u'_context_quota_class': None,
    u'_context_read_deleted': u'no',
    u'_context_remote_address': u'10.0.2.15',
    u'_context_request_id': u'req-d68b36e0-9233-467f-9afb-d81435d64d66',
    u'_context_roles': [u'admin'],
    u'_context_timestamp': u'2012-05-08T20:23:41.425105',
    u'_context_user_id': u'1e3ce043029547f1a61c1996d1a531a2',
    u'event_type': u'akanda.bandwidth.used',
    u'message_id': u'dae6f69c-00e0-41c0-b371-41ec3b7f4451',
    u'payload': {u'external': {u'out': {u'packets': 1234,
                                        u'bytes': 22434,
                                        },
                               u'in': {u'packets': 88,
                                       u'bytes': 89420,
                                       },
                               },
                 u'internal': {u'out': {u'packets': 4567,
                                        u'bytes': 82984,
                                        },
                               u'in': {u'packets': 77,
                                       u'bytes': 98982,
                                       },
                               },
                 },
    u'priority': u'INFO',
    u'tenant_id': u'7c150a59fe714e6f9263774af9688f0e',
    u'timestamp': u'2012-05-08 20:23:48.028195',
    }

EXPECTED_COUNTERS = {
    'akanda.bandwidth:external.out.packets': 1234,
    'akanda.bandwidth:external.out.bytes': 22434,
    'akanda.bandwidth:external.in.packets': 88,
    'akanda.bandwidth:external.in.bytes': 89420,
    'akanda.bandwidth:internal.out.packets': 4567,
    'akanda.bandwidth:internal.out.bytes': 82984,
    'akanda.bandwidth:internal.in.packets': 77,
    'akanda.bandwidth:internal.in.bytes': 98982,
    }


class TestNotifications(unittest.TestCase):

    def setUp(self):
        self.bw_handler = NetworkBandwidthNotification()

    @staticmethod
    def _find_counter(counters, name):
        for counter in counters:
            if counter.name == name:
                return counter
        return None

    def test_default_exchange_topics(self):
        topics = NetworkBandwidthNotification.get_exchange_topics(cfg.CONF)
        assert len(topics) == 1

        got_exchange = topics[0].exchange
        got_topics = topics[0].topics
        expected_exchange = 'akanda'
        expected_topics = set(['notifications.info'])

        assert got_exchange == expected_exchange
        assert got_topics == expected_topics

    def test_multiple_exchange_topics(self):
        CONF = mock.Mock()
        CONF.akanda_notification_exchange = 'the_exchange'
        CONF.akanda_notification_topics = ['topic1', 'topic2']
        topics = NetworkBandwidthNotification.get_exchange_topics(CONF)
        assert len(topics) == 1

        got_exchange = topics[0].exchange
        got_topics = topics[0].topics
        expected_exchange = 'the_exchange'
        expected_topics = set(['topic1.info', 'topic2.info'])

        assert got_exchange == expected_exchange
        assert got_topics == expected_topics

    def _check_notification(self, message, expected_counters):
        got = list(
            self.bw_handler.process_notification(message)
            )
        assert len(got) == len(expected_counters)
        for name in expected_counters:
            counter = TestNotifications._find_counter(got, name)
            assert counter is not None

            got_volume = counter.volume
            expected_volume = expected_counters[name]
            assert got_volume == expected_volume

            got_project_id = counter.project_id
            expected_project_id = message['tenant_id']
            assert got_project_id == expected_project_id

            got_timestamp = counter.timestamp
            expected_timestamp = message['timestamp']
            assert got_timestamp == expected_timestamp

    def test_process_notification(self):
        self._check_notification(BW_NOTIFICATION, EXPECTED_COUNTERS)

    def test_process_notification_alt(self):
        self._check_notification(BW_NOTIFICATION_ALT, EXPECTED_COUNTERS)
