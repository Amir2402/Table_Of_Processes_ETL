from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from processExtract import get_processes_list 
from dotenv import load_dotenv 
import os 
import json 
import time 
import sys 

def produce_messages() : 
    load_dotenv() 
    server = os.getenv('KAF_SERVER')
    my_topic = os.getenv('TOPIC_NAME') 

    try :
        producer = KafkaProducer(bootstrap_servers = [server] , 
                            value_serializer = lambda v : json.dumps(v).encode('utf-8') , 
                            key_serializer = lambda v : json.dumps(v).encode('utf-8')
                            )
        
        while True : 
            
            try :        
                
                for process in get_processes_list() : 
                    producer.send(topic = my_topic , key = {"id" : 1} , value = process)
                producer.flush()
                time.sleep(2)
                
            except KeyboardInterrupt : 
                print('producer stopped')
                sys.exit()

    except NoBrokersAvailable : 
        print('NO BROKERS AVAILABLE !!!!')
        sys.exit() 

if __name__ == '__main__'  : 
    produce_messages()
    