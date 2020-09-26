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
    def __init__(self, queue= 'MQ', host = 'localhost', port = 5672, 
                 username = 'guest', password = 'guest', routingKey = 'MQ', exchange = ''):
        self.queue = queue
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.routingKey = routingKey
        self.exchange = exchange

class RabbitMq():
    
    #Creattion of message queue using RabbitMqConfig
    def __init__(self, server):
        self.server = server
        self.response = None
        self.cases_response = None
        self.hospitals_response = None
        self.inventory_response = None
        self._credentials = pika.PlainCredentials(self.server.username, self.server.password)
        self._connectParameters = pika.ConnectionParameters(self.server.host, self.server.port,
                                                            '/', self._credentials)
        self._connection = pika.BlockingConnection(self._connectParameters)
        self._channel = self._connection.channel()
        self._result = self._channel.queue_declare(queue=self.server.queue, durable= True)
        self._callback_queue = self._result.method.queue

        self._channel.basic_consume(queue=self._callback_queue, 
                                    on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id: 
            self.response = str(body.decode())
            self.cases_response = None
            self.hospitals_response = None
            self.inventory_response = None


    def publish(self, msg):

        self.corr_id = str(uuid.uuid4())
        self._channel.basic_publish(exchange=self.server.exchange,
                                    routing_key=self.server.routingKey,
                                    body=str(msg),
                                    properties=pika.BasicProperties(
                                        reply_to=self._callback_queue,
                                        correlation_id=self.corr_id,
                                        delivery_mode=2
                                    ))
        print('[x] Sent message to execute: {}'.format(msg))

        while self.response != msg:
            self._connection.process_data_events()     
        
        return str(self.response)
    
    def close(self):
        self._connection.close()

if __name__ == "__main__":

    # serverConfig = RabbitMqConfigure(queue= 'RBMQ', 
    #                            host= '192.168.0.148',
    #                            port= 5672,
    #                            username= 'rabbituser',
    #                            password='rabbit1234',
    #                            routingKey= 'RBMQ', 
    #                            exchange= '')
    serverConfig = RabbitMqConfigure()
    messageQueue = RabbitMq(serverConfig)
    cases_response = messageQueue.publish(msg='cases')
    hospitals_response = messageQueue.publish(msg='hospitals')
    inventory_response = messageQueue.publish(msg='inventory')
    
    print(" [.] Response for cases processing: %s" % cases_response)
    print(" [.] Response for hospitals processing: %s" % hospitals_response)
    print(" [.] Response for inventory processing: %s" % inventory_response)

    # shared_resource_lock=threading.Lock() 
    # param_list = ['cases', 'hospitals']#, 'inventory']

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(messageQueue.publish, param) for param in param_list]

    #     executor.shutdown()
    
    # return_values = [f.result() for f in futures]
    # print(return_values)

    messageQueue.close()