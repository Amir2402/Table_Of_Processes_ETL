from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError , NoBrokersAvailable
import os 
from dotenv import load_dotenv
import sys 

class topic_creator : 
    server = None 
    my_topic = None 
    
    def __init__(self , server , my_topic):
        self.server = server  
        self.my_topic = my_topic

    def create_topic(self) : 
        
        try : 
            admin_client = KafkaAdminClient(bootstrap_servers = self.server) 
            topic_config = {
            'cleanup.policy' : 'delete' , 
            'retention.ms' : '2000' 
            }
            new_topic = NewTopic(name = self.my_topic , 
                                num_partitions= 3 , 
                                replication_factor= 1 , 
                                topic_configs =  topic_config)
            admin_client.create_topics(new_topics = [new_topic])
            admin_client.close()

        except NoBrokersAvailable :
            print('NO BROKERS AVAILABLE !!!')
            sys.exit()
            
        except TopicAlreadyExistsError :
            admin_client.close()    
            top.delete_topic()
            admin_client = KafkaAdminClient(bootstrap_servers = self.server)
            admin_client.create_topics(new_topics = [new_topic])
            admin_client.close()  
               
    def getl_list_of_topics(self) :
        
        try : 
            admin_client = KafkaAdminClient(bootstrap_servers = self.server) 
            print(admin_client.list_topics())

        except NoBrokersAvailable: 
            print('NO BROKERS AVAILABLE !!!')
            sys.exit()
        
        else :
            admin_client.close()

    def delete_topic(self) : 
        
        try : 
            admin_client = KafkaAdminClient(bootstrap_servers = self.server) 
            admin_client.delete_topics([self.my_topic])

        except NoBrokersAvailable: 
            print('NO BROKERS AVAILABLE !!!')
            sys.exit()
        
        else : 
            admin_client.close()

if __name__ == '__main__' : 
    load_dotenv() 
    server = os.getenv('KAF_SERVER')
    my_topic = os.getenv('TOPIC_NAME')
    top = topic_creator(server , my_topic) 
    top.create_topic()
    print('topic created succefully')
    print('list of topics after adding yours')
    top.getl_list_of_topics()
    


