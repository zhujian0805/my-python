from kafka import KafkaConsumer
import avro.schema
import avro.io
import io
import sys

# To consume messages
consumer = KafkaConsumer(
    '%s' % sys.argv[1],
    group_id='%s' % sys.argv[2],
    bootstrap_servers=['%s:9092' % sys.argv[3]])

schema_path = "user.avsc"
schema = avro.schema.parse(open(schema_path).read())

for msg in consumer:
    bytes_reader = io.BytesIO(msg.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    user1 = reader.read(decoder)
    print user1
