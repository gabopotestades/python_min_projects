import pika
import uuid

class MetaClass(type):

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqConfigure(metaclass= MetaClass):

    #Initialize message queue parameters
    def __init__(self, queue= '', host = 'localhost', port = 5672, 
                 username = 'guest', password = 'guest', routingKey = '', 
                 exchange = 'topic_logs', exchange_type='topic'):
        self.queue = queue
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.routingKey = routingKey
        self.exchange = exchange
        self.exchange_type = exchange_type

class RabbitMq():
    
    #Creation of message queue using RabbitMqConfig
    def __init__(self, server):
        self.server = server
        self.response = None
        self.processes = ['cases', 'hospitals', 'inventory']
        self.requeue = ['cases-requeue', 'hospitals-requeue', 'inventory-requeue']
        self._credentials = pika.PlainCredentials(self.server.username, self.server.password)
        self._connectParameters = pika.ConnectionParameters(self.server.host, self.server.port,
                                                            '/', self._credentials)
        self._connection = pika.BlockingConnection(self._connectParameters)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self.server.exchange, exchange_type=self.server.exchange_type)
        
        self._result = self._channel.queue_declare(queue=self.server.queue, durable= True)
        self._callback_queue = self._result.method.queue

        #self._channel.basic_qos(prefetch_count=3)
        self._channel.basic_consume(queue=self._callback_queue, 
                                    on_message_callback=self.on_response, auto_ack=True)

        self._channel.queue_bind(exchange=self.server.exchange, 
                            queue=self._result.method.queue,
                            routing_key=self._callback_queue)
        #self._channel.start_consuming()

    def on_response(self, ch, method, props, body):

        response = str(body.decode())

        if self.corr_id == props.correlation_id:
            if response in self.processes: 
                    self.response = 'succeeded...'
            elif response in self.requeue: 
                    self.response = 'processing requeue...'
            elif 'failed' in response:
                    self.response = response

    def publish(self, msg, routing_key):
        
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self._channel.basic_publish(exchange=self.server.exchange,
                                    routing_key=routing_key,
                                    body=str(msg),
                                    properties=pika.BasicProperties(
                                        reply_to=self._callback_queue,
                                        correlation_id=self.corr_id,
                                        delivery_mode=2
                                    ))
        print('[*] Sent message to execute: {}'.format(msg))

        while self.response == None:
            self._connection.process_data_events()     
        
        return str(self.response)
    
    def close(self):
        self._connection.close()

if __name__ == "__main__":

    serverConfig = RabbitMqConfigure(host= '192.168.0.148', 
                                     port= 5672,
                                     username= 'rabbituser', 
                                     password= 'rabbit1234')
    #serverConfig = RabbitMqConfigure(queue='response_queue')
    messageQueue = RabbitMq(serverConfig)

    cases_response = messageQueue.publish(msg='cases', routing_key = 'light.cases')
    print(" [.] Response for cases: %s" % cases_response)
    hospitals_response = messageQueue.publish(msg='hospitals', routing_key = 'heavy.hospitals')
    print(" [.] Response for hospitals: %s" % hospitals_response)
    inventory_response = messageQueue.publish(msg='inventory', routing_key = 'light.inventory')
    print(" [.] Response for inventory: %s" % inventory_response)

    if 'fail' in cases_response:

        print(" [x] Cases process failed, requeing in other queue...") 
        cases_response = messageQueue.publish(msg='cases-requeue', routing_key = 'heavy.cases') 
        print(" [.] Response for cases requeue: %s" % cases_response)

    if 'fail' in hospitals_response:

        print(" [x] Hospitals process failed, requeing in other queue...")  
        hospitals_response = messageQueue.publish(msg='hospitals-requeue', routing_key = 'light.hospitals')
        print(" [.] Response for hospitals requeue: %s" % hospitals_response)

    if 'fail' in inventory_response:

        print(" [x] Inventory process failed, requeing in other queue...")  
        inventory_response = messageQueue.publish(msg='inventory-requeue', routing_key = 'heavy.inventory')
        print(" [.] Response for inventory requeue: %s" % inventory_response)

    print('\nSummary: ')
    print('Cases: ' + ('Success' if not 'fail' in cases_response else 'Fail'))
    print('Hospitals: ' + ('Success' if not 'fail' in hospitals_response else 'Fail'))
    print('Inventory: ' + ('Success' if not 'fail' in inventory_response else 'Fail'))

    messageQueue.close()