"""Handler for producing counter messages from Akanda notifications.
"""

from ceilometer import counter, plugin
from ceilometer.openstack.common import cfg
from ceilometer.openstack.common import log as logging


OPTS = [
    cfg.StrOpt('akanda_notification_exchange',
               default='akanda',
               help="Exchange name for Akanda notifications"),
    cfg.ListOpt('akanda_notification_topics',
                default=['notifications'],
                help="Topic name for Akanda notifications"),
    ]

cfg.CONF.register_opts(OPTS)

LOG = logging.getLogger(__name__)


class NetworkBandwidthNotification(plugin.NotificationBase):

    def get_event_types(self):
        return ['akanda.bandwidth.used']

    @staticmethod
    def get_exchange_topics(conf):
        """Returns a sequence of ExchangeTopics defining the exchange and
        topics to be connected to this plugin."""
        return [
            plugin.ExchangeTopics(
                exchange=conf.akanda_notification_exchange,
                topics=set(topic + '.info'
                           for topic in conf.akanda_notification_topics)),
            ]

    def process_notification(self, message):
        LOG.info('akanda network notification %r', message)

        # TODO (sberler): handle arbitrary nested dictionaries instead
        # of just two levels.
        for type_ in message['payload']:
            for subtype in message['payload'][type_]:
                yield counter.Counter(
                    source='?',
                    name='akanda.bandwidth:%s.%s' % (type_, subtype),
                    type=counter.TYPE_DELTA,
                    volume=message['payload'][type_][subtype],
                    project_id=message['tenant_id'],
                    timestamp=message['timestamp'],
                    user_id=None,
                    resource_id=None,
                    resource_metadata={},
                    )
