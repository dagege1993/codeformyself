from kafka import KafkaConsumer

consumer = KafkaConsumer('test', group_id='m1', bootstrap_servers=['jkbigdata:9092'])
for msg in consumer:
	print(msg)
	consumer.close()
