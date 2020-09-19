import pika
import ds_ParallelProcessing

class MetaClass(type):

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqServerConfigure(metaclass= MetaClass):

    #Initialize message queue server parameters
    def __init__(self, host= 'localhost', port = 5672, 
                 username= 'guest', password= 'guest', queue= 'MainQ'):
        self.queue = queue
        self.host = host
        self.port = port
        self.username = username
        self.password = password

class RabbitMqServer():

    #Initiliaze server using RabbitMqServerConfigure 
    def __init__(self, server):
        self.server = server
        self._credentials = pika.PlainCredentials(self.server.username, self.server.password)
        self._connectParameters = pika.ConnectionParameters(self.server.host, self.server.port,
                                                            '/', self._credentials)
        self._connection = pika.BlockingConnection(self._connectParameters)
        # self._connection = pika.BlockingConnection(pika.ConnectionParameters(self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def callback(self, ch, method, properties, body):
        msg = str(body.decode())
        if msg == 'cases':
            print("Executing the cases task...")
            casesInformationProcess = ds_ParallelProcessing.caseProcess(1, 'DS_Case_Summary.txt')
            casesInformationProcess.start()
        elif msg == 'hospitals':
            print("Executing the hospitals task...")
            hospitalsInformationProcess = ds_ParallelProcessing.hospitalsProcess(2, 'DS_Hospital_Summary.txt')
            hospitalsInformationProcess.start()
        elif msg == 'inventory':
            print("Executing the inventory task...")
            inventoryInformationProcess = ds_ParallelProcessing.inventoryProcess(3, 'DS_Inventory_Summary.txt')
            inventoryInformationProcess.start()
            
    def startServer(self):
        self._channel.basic_consume(self.server.queue, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()

if __name__ == '__main__':

    serverConfig = RabbitMqServerConfigure(host= '192.168.0.148', port= 5672,
                                           username= 'rabbituser', password='rabbit1234', 
                                           queue= 'MainQ')
    # serverConfig = RabbitMqServerConfigure()
    messageQueueServer = RabbitMqServer(serverConfig)
    messageQueueServer.startServer()
