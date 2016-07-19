hadoop jar /opt/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -file mapper.py -mapper mapper.py -file reducer.py -reducer reducer.py  -input $1 -output $2
