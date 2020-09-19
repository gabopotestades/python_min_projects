import pika

class MetaClass(type):

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqConfigure(metaclass= MetaClass):

    #Initialize message queue parameters
    def __init__(self, queue= 'MainQ', host = 'localhost', 
                 routingKey = 'MainQ', exchange = ''):
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange

class RabbitMq():
    
    #Creattion of message queue using RabbitMqConfig
    def __init__(self, server):
        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def publish(self, payload):
        self._channel.basic_publish(exchange=self.server.exchange,
                                    routing_key=self.server.routingKey,
                                    body=str(payload))
        print('Published message: {}'.format(payload))
        self._connection.close()

if __name__ == "__main__":

    serverConfig = RabbitMqConfigure(queue= 'MainQ', 
                               host = 'localhost',           
                               routingKey = 'MainQ', 
                               exchange = '')
    messageQueue = RabbitMq(serverConfig)
    messageQueue.publish(payload='Test')
