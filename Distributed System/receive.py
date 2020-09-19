import pika

class MetaClass(type):

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqServerConfigure(metaclass= MetaClass):

    #Initialize message queue server parameters
    def __init__(self, host= 'localhost', queue= 'MainQ'):
        self.host = host
        self.queue = queue

class RabbitMqServer():

    #Initiliaze server using RabbitMqServerConfigure 
    def __init__(self, server):
        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def startServer(self):
        self._channel.basic_consume(self.server.queue, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()

if __name__ == '__main__':
    serverConfig = RabbitMqServerConfigure(host= 'localhost', queue= 'MainQ')
    messageQueueServer = RabbitMqServer(serverConfig)
    messageQueueServer.startServer()
