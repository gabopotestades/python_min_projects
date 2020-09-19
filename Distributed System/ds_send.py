import pika

class MetaClass(type):

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqConfigure(metaclass= MetaClass):

    #Initialize message queue parameters
    def __init__(self, queue= 'MainQ', host = 'localhost', port = 5672, 
                 username = 'guest', password = 'guest', routingKey = 'MainQ', exchange = ''):
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
        self._credentials = pika.PlainCredentials(self.server.username, self.server.password)
        self._connectParameters = pika.ConnectionParameters(self.server.host, self.server.port,
                                                            '/', self._credentials)
        self._connection = pika.BlockingConnection(self._connectParameters)
        # self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def publish(self, msg):
        self._channel.basic_publish(exchange=self.server.exchange,
                                    routing_key=self.server.routingKey,
                                    body=str(msg))
        print('Sent message to execute: {}'.format(msg))
    
    def close(self):
        self._connection.close()

if __name__ == "__main__":

    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('103.231.240.131', '10148', 'gpotestades', 'fTINjQlZ')

    # stdin, stdout, stderr = ssh.exec_command('ls')
    # lines = stdout.readlines()
    # print(lines)

    serverConfig = RabbitMqConfigure(queue= 'MainQ', 
                               host= '192.168.0.148',
                               port= 5672,
                               username= 'rabbituser',
                               password='rabbit1234',
                               routingKey= 'MainQ', 
                               exchange= '')
    # serverConfig = RabbitMqConfigure()
    messageQueue = RabbitMq(serverConfig)
    messageQueue.publish(msg='cases')
    messageQueue.publish(msg='hospitals')
    messageQueue.publish(msg='inventory')
    messageQueue.close()