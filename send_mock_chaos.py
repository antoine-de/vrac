import calendar
import uuid
from datetime import datetime
from kombu.connection import BrokerConnection
from kombu.entity import Exchange
from kombu.pools import producers
from retrying import Retrying
import chaos_pb2
import gtfs_realtime_pb2


#we need to generate a unique topic not to have conflict between tests
rt_topic = 'rt_test_{}'.format(uuid.uuid1())


class RabbitMQCnx(object):
    """
    Mock a chaos disruption message, in order to check the api
    """
    def _get_producer(self):
        producer = producers[self.mock_chaos_connection].acquire(block=True, timeout=2)
        self._connections.add(producer.connection)
        return producer

    def __init__(self, rt_topic):
        self.rt_topic = rt_topic
        self.mock_chaos_connection = BrokerConnection("pyamqp://guest:guest@localhost:5672")
        self._connections = {self.mock_chaos_connection}
        self._exchange = Exchange('navitia', durable=True, delivry_mode=2, type='topic')
        self.mock_chaos_connection.connect()

    def __del__(self):
        #we need to release the amqp connection
        self.mock_chaos_connection.release()

    def _publish(self, item):
        with self._get_producer() as producer:
            producer.publish(item, exchange=self._exchange, routing_key=self.rt_topic, declare=[self._exchange])

    def send_mock(self, item):
        self._publish(item)


def date_to_timestamp(date):
    """
    convert a datatime objet to a posix timestamp (number of seconds from 1070/1/1)
    """
    return int(calendar.timegm(date.utctimetuple()))

def str_to_time_stamp(str):
    """
    convert a string to a posix timestamp
    the string must be in the YYYYMMDDTHHMMSS format
    like 20170534T124500
    """
    date = datetime.strptime(str, "%Y%m%dT%H%M%S")

    return date_to_timestamp(date)

def make_mock_chaos_item(disruption_name, impacted_obj, impacted_obj_type, start=None, end=None,
                         message_text='default_message', is_deleted=False, blocking=False,
                         start_period="20100412T165200", end_period="20200412T165200"):
    feed_message = gtfs_realtime_pb2.FeedMessage()
    feed_message.header.gtfs_realtime_version = '1.0'
    feed_message.header.incrementality = gtfs_realtime_pb2.FeedHeader.DIFFERENTIAL
    feed_message.header.timestamp = 0

    feed_entity = feed_message.entity.add()
    feed_entity.id = disruption_name
    feed_entity.is_deleted = is_deleted

    disruption = feed_entity.Extensions[chaos_pb2.disruption]

    disruption.id = disruption_name
    disruption.cause.id = "CauseTest"
    disruption.cause.wording = "CauseTest"
    disruption.reference = "DisruptionTest"
    disruption.publication_period.start = str_to_time_stamp(start_period)
    disruption.publication_period.end = str_to_time_stamp(end_period)

    # Tag
    tag = disruption.tags.add()
    tag.name = "rer"
    tag.id = "rer"
    tag = disruption.tags.add()
    tag.name = "metro"
    tag.id = "rer"

    if not impacted_obj or not impacted_obj_type:
        return feed_message.SerializeToString()

    # Impacts
    impact = disruption.impacts.add()
    impact.id = "impact_" + disruption_name + "_1"
    enums_impact = gtfs_realtime_pb2.Alert.DESCRIPTOR.enum_values_by_name
    if blocking:
        impact.severity.effect = enums_impact["NO_SERVICE"].number
        impact.severity.id = 'blocking'
        impact.severity.priority = 10
        impact.severity.wording = "blocking"
        impact.severity.color = "#FFFF00"
    else:
        impact.severity.effect = enums_impact["UNKNOWN_EFFECT"].number
        impact.severity.id = ' not blocking'
        impact.severity.priority = 1
        impact.severity.wording = "not blocking"
        impact.severity.color = "#FFFFF0"

    # ApplicationPeriods
    application_period = impact.application_periods.add()
    application_period.start = str_to_time_stamp(start_period)
    application_period.end = str_to_time_stamp(end_period)

    # PTobject
    type_col = {
        "network": chaos_pb2.PtObject.network,
        "stop_area": chaos_pb2.PtObject.stop_area,
        "line": chaos_pb2.PtObject.line,
        "line_section": chaos_pb2.PtObject.line_section,
        "route": chaos_pb2.PtObject.route,
        "stop_point": chaos_pb2.PtObject.stop_point
    }

    ptobject = impact.informed_entities.add()
    ptobject.uri = impacted_obj
    ptobject.pt_object_type = type_col.get(impacted_obj_type, chaos_pb2.PtObject.unkown_type)
    if ptobject.pt_object_type == chaos_pb2.PtObject.line_section:
        line_section = ptobject.pt_line_section
        line_section.line.uri = impacted_obj
        line_section.line.pt_object_type = chaos_pb2.PtObject.line
        pb_start = line_section.start_point
        pb_start.uri = start
        pb_start.pt_object_type = chaos_pb2.PtObject.stop_area
        pb_end = line_section.end_point
        pb_end.uri = end
        pb_end.pt_object_type = chaos_pb2.PtObject.stop_area

    # Message with one channel and one channel type: sms
    message = impact.messages.add()
    message.text = message_text
    message.channel.id = "sms"
    message.channel.name = "sms"
    message.channel.max_size = 60
    message.channel.content_type = "text"
    message.channel.types.append(chaos_pb2.Channel.sms)

    # Message with one channel and two channel types: web and email
    message = impact.messages.add()
    message.text = message_text
    message.channel.name = "email"
    message.channel.id = "email"
    message.channel.max_size = 250
    message.channel.content_type = "html"
    message.channel.types.append(chaos_pb2.Channel.web)
    message.channel.types.append(chaos_pb2.Channel.email)

    return feed_message.SerializeToString()


def make_mock_kirin_item(vj_id, date, status='delayed', new_stop_time_list=[]):
    feed_message = gtfs_realtime_pb2.FeedMessage()
    feed_message.header.gtfs_realtime_version = '1.0'
    feed_message.header.incrementality = gtfs_realtime_pb2.FeedHeader.DIFFERENTIAL
    feed_message.header.timestamp = 0

    entity = feed_message.entity.add()
    entity.id = "96231_2015-07-28_0"
    trip_update = entity.trip_update

    trip = trip_update.trip
    trip.trip_id = vj_id  #
    trip.start_date = date

    if status == 'canceled':
        trip.schedule_relationship = gtfs_realtime_pb2.TripDescriptor.CANCELED
    elif status == 'delayed':
        trip.schedule_relationship = gtfs_realtime_pb2.TripDescriptor.SCHEDULED
        for st in new_stop_time_list:
            stop_time_update = trip_update.stop_time_update.add()
            stop_time_update.stop_id = st[0]
            stop_time_update.arrival.time = st[1]
            stop_time_update.departure.time = st[2]
    else:
        #TODO
        pass

    return feed_message.SerializeToString()

rabbit_cnx = RabbitMQCnx('topic12')

# mock = make_mock_chaos_item("blocking_line_disruption", "stopB", "stop_area")
# mock = make_mock_kirin_item("vjA", "20120614", 'canceled')
# #
# mock = make_mock_kirin_item("vjA", "20120614", 'delayed',
#                             [("stop_point:stopB", str_to_time_stamp("20120614T080224"), str_to_time_stamp("20120614T080224")),
#                              ("stop_point:stopA", str_to_time_stamp("20120614T080400"), str_to_time_stamp("20120614T080400"))])
#
# mock = make_mock_kirin_item("vjB", "20120614", 'delayed',
#            [("stop_point:stopB", str_to_time_stamp("20120614T180224"), str_to_time_stamp("20120614T180225")),
#             ("stop_point:stopA", str_to_time_stamp("20120614T180400"), str_to_time_stamp("20120614T180400"), "bob's in the place")])

mock = make_mock_chaos_item("bobette_the_disruption", "A",
                            "line_section", start="stopB", end="stopA",
                            start_period="20120614T070000", end_period="20120624T170000",
                            blocking=True)

rabbit_cnx.send_mock(mock)

