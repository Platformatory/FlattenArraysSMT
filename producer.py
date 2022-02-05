import uuid
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer


value_schema_str = """
{
   "namespace": "my.test",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     },
     {
       "default": null,
       "name": "recordIds",
       "type": [
         "null",
         {
           "items": "string",
           "type": "array"
         }
       ]
     }
   ]
}
"""

key_schema_str = """
{
   "namespace": "my.test",
   "name": "key",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     }
   ]
}
"""

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


avroProducer = AvroProducer({
    'bootstrap.servers': 'xxx-zzzzz.us-west4.gcp.confluent.cloud:9092',
    'on_delivery': delivery_report,
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'YYYYYYYYYY',
    'sasl.password': 'XXXX',
    'schema.registry.basic.auth.credentials.source': 'USER_INFO',
    'schema.registry.basic.auth.user.info': 'USERNAME:PASSWORD',
    'schema.registry.url': 'https://xxx-zzzzz.us-central1.gcp.confluent.cloud'
    }, default_key_schema=key_schema, default_value_schema=value_schema)


record_ids = [
    "foo",
    "bar",
    "baz",
]

for i in range(1,10):
    random_str = str(uuid.uuid4())
    value = {"name": "Value-" + random_str, "recordIds": record_ids}
    key = {"name": random_str}
    avroProducer.produce(topic='test-topic-1', value=value, key=key)

avroProducer.flush()