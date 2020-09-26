import pika
import time
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
                 username= 'guest', password= 'guest', queue= 'MQ', exchange = ''):
        self.queue = queue
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.exchange = exchange

class RabbitMqServer():

    #Initiliaze server using RabbitMqServerConfigure 
    def __init__(self, server):
        self.server = server
        self._credentials = pika.PlainCredentials(self.server.username, self.server.password)
        self._connectParameters = pika.ConnectionParameters(self.server.host, self.server.port,
                                                            '/', self._credentials)
        self._connection = pika.BlockingConnection(self._connectParameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue, durable=True)

    def callback(self, ch, method, properties, body):

        msg = str(body.decode())

        try:     
            
            response = msg #'Processed ' + msg
            ch.basic_publish(exchange=self.server.exchange,
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(
                             correlation_id=properties.correlation_id),
                             body=str(response))
            ch.basic_ack(delivery_tag=method.delivery_tag)  
            #print(' [.] ' + response)
            
            if msg == 'cases':
                cases_start = time.time()

                print(" [x] Executing the cases task...")
                casesInformationProcess = ds_ParallelProcessing.caseProcess(1, 'DS_Case_Summary.txt')
                casesInformationProcess.start()
                casesInformationProcess.join()

                cases_end = time.time() - cases_start
                f = open('Cases_Time.txt', 'a+')
                f.write(str(cases_end) + '\n')
                f.close()

                print(" [.] Succeeded in processing the cases task...")

            elif msg == 'hospitals':

                hospitals_start = time.time()

                print(" [x] Executing the hospitals task...")
                hospitalsInformationProcess = ds_ParallelProcessing.hospitalsProcess(2, 'DS_Hospital_Summary.txt')
                hospitalsInformationProcess.start()
                hospitalsInformationProcess.join()

                hospitals_end = time.time() - hospitals_start 
                f = open('Hospitals_Time.txt', 'a+')
                f.write(str(hospitals_end) + '\n')
                f.close()

                print(" [.] Succeeded in processing the hospitals task...")

            elif msg == 'inventory':

                inventory_start = time.time()

                print(" [x] Executing the inventory task...")
                inventoryInformationProcess = ds_ParallelProcessing.inventoryProcess(3, 'DS_Inventory_Summary.txt')
                inventoryInformationProcess.start()
                inventoryInformationProcess.join()

                inventory_end = time.time() - inventory_start 
                f = open('Inventory_Time.txt', 'a+')
                f.write(str(inventory_end) + '\n')
                f.close()

                print(" [.] Succeeded in processing the inventory task...")

        except Exception as e:

            response = str(e)
            ch.basic_publish(exchange=self.server.exchange,
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(
                             correlation_id=properties.correlation_id),
                             body=str(response))
            ch.basic_nack(delivery_tag=method.delivery_tag) 
 
    def startServer(self):
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(self.server.queue, on_message_callback=self.callback)
        print('[*] Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()

if __name__ == '__main__':

    # serverConfig = RabbitMqServerConfigure(host= '192.168.0.148', port= 5672,
    #                                        username= 'rabbituser', password= 'rabbit1234', 
    #                                        queue= 'RBMQ', exchange= '')
    serverConfig = RabbitMqServerConfigure()
    messageQueueServer = RabbitMqServer(serverConfig)
    messageQueueServer.startServer()