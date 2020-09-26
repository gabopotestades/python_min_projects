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
        self._credentials = pika.PlainCredentials(self.server.username, self.server.password)
        self._connectParameters = pika.ConnectionParameters(self.server.host, self.server.port,
                                                            '/', self._credentials)
        self._connection = pika.BlockingConnection(self._connectParameters)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self.server.exchange, exchange_type=self.server.exchange_type)
        
        self._result = self._channel.queue_declare(queue=self.server.queue, durable= True, exclusive=True)
        self._callback_queue = self._result.method.queue

        self._channel.basic_consume(queue=self._callback_queue, 
                                    on_message_callback=self.on_response, auto_ack=True)
        self._channel.queue_bind(exchange=self.server.exchange, 
                            queue=self._result.method.queue,
                            routing_key=self._callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id: 
            self.response = str(body.decode())

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
        print('[x] Sent message to execute: {}'.format(msg))

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

    #serverConfig = RabbitMqConfigure(queue='')
    messageQueue = RabbitMq(serverConfig)
    cases_response = messageQueue.publish(msg='cases', routing_key = 'light.cases')
    hospitals_response = messageQueue.publish(msg='hospitals', routing_key = 'heavy.hospitals')
    inventory_response = messageQueue.publish(msg='inventory', routing_key = 'light.inventory')
    
    print(" [.] Response for cases processing: %s" % cases_response)
    print(" [.] Response for hospitals processing: %s" % hospitals_response)
    print(" [.] Response for inventory processing: %s" % inventory_response)

    messageQueue.close()