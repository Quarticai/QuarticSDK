from confluent_kafka import Consumer
import json
import datetime
import pytz
from pytz import timezone
from confluent_kafka.cimpl import Producer
from confluent_kafka import Consumer
localtz = timezone('UTC')
import pandas as pd
from pydantic import BaseModel
from typing import Any, List
from collections import deque
from functools import wraps
import logging
import time
import os
import yaml
import abc
import fastparquet as fp

class FlatDataPoint(BaseModel):
    """
    Base class for data point. The data in this class is stored in `data` property. This will typically contain
    data for multiple tags for a given timestamp. This can also contain any Exception that were raised during the
    data IO.
    """
    edgeconnector: int
    timestamp: int
    tag: str
    value: float



class DataConsumer(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.df = pd.DataFrame([])
        self.queue: List[FlatDataPoint] = deque()
        self.window_duration=None
        self.tags = []
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.app_start_time = None
        self.batch_start = None
        self.partition_mins = None
        self.kafka_producer = Producer(self.get_producer_config())
        self.last_known_value = {}
        

    def read_config(self):
        file_path = os.getenv('CONFIG_FILE')
        if not file_path:
            file_path = 'config.yaml'
        if not os.path.exists(file_path):
            raise NotImplementedError("Config File does not exist")
        with open(file_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data


    def get_producer_config(self):
        return self.read_config()['ProducerConfig']


    def get_consumer_config(self):
        return self.read_config()['ConsumerConfig']


    def write(self, output_tag, edge_connector, value):
        def delivery_callback( err, msg ):
            if err:
                self.log.exception(err)
            else:
                self.log.debug('written')
        

        msg = FlatDataPoint(timestamp=int(time.time()*1000), tag= str(output_tag), edgeconnector=edge_connector, value=value)
        self.kafka_producer.produce('softtags', json.dumps(msg.model_dump()),
                                                        key= "softtags",
                                                        on_delivery=delivery_callback)
        self.kafka_producer.flush()

    @abc.abstractmethod
    def compute(self, df):
        pass

    def update_df(self, msg):
        df = pd.DataFrame([msg])
        file = 'example.parquet'
        kwargs = {
            'partition_on': ['partition_block'],
            "file_scheme": "hive"
        }

        if os.path.exists(file):
            kwargs['append'] =  True

        fp.write(file, df, **kwargs)

    def process_message(self, msg):
        msg = json.loads(msg.value())
        dp = FlatDataPoint(**msg)
        if dp.tag in self.tags:
            self.last_known_value[dp.tag] = dp.value
            if self.partition_mins:
                partition_block = (time.time()-self.app_start_time)//(self.partition_mins *60)
            else:
                partition_block = 0
            self.update_df({'timestamp': dp.timestamp, 'tag_id': dp.tag, 'value': dp.value, 'partition_block': partition_block})


    def check_and_run_compute_if_required(self):
        if time.time()-self.batch_start < self.window_duration*60:
            return
        df = pd.read_parquet('example.parquet')
        self.compute(df)
        self.batch_start = time.time()

    def read(self):
        consumer = Consumer(self.get_consumer_config())
        consumer.subscribe(["flat_telemetry"])
        while True:
            msg = consumer.poll(1.0)
            if msg is not None:
                self.process_message(msg)

            self.check_and_run_compute_if_required()


    def start(self, duration, tags = [], partition_mins = 0):
        self.window_duration = duration
        self.tags = tags
        self.app_start_time = time.time()
        self.batch_start = time.time()
        self.partition_mins=partition_mins
        self.read()