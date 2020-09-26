import sys
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
    def __init__(self, queue= '', host = 'localhost', port = 5672, 
                 username = 'guest', password = 'guest', routingKey = '', 
                 exchange = 'topic_logs', exchange_type='topic'):
        self.queue = queue
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.routing_key = routingKey
        self.exchange = exchange
        self.exchange_type = exchange_type

class RabbitMqServer():

    #Initiliaze server using RabbitMqServerConfigure 
    def __init__(self, server):
        self.server = server
        self._credentials = pika.PlainCredentials(self.server.username, self.server.password)
        self._connectParameters = pika.ConnectionParameters(self.server.host, self.server.port,
                                                            '/', self._credentials)
        self._connection = pika.BlockingConnection(self._connectParameters)
        self._channel = self._connection.channel()

        self._channel.exchange_declare(exchange=self.server.exchange, exchange_type=self.server.exchange_type)
        self.result = self._channel.queue_declare(queue=self.server.queue, durable=True)
        self._channel.queue_bind(exchange=self.server.exchange, 
                                 queue=self.result.method.queue,
                                 routing_key=self.server.routing_key)

    def callback(self, ch, method, properties, body):

        msg = str(body.decode())

        try:     
            
            response = msg
            
            if msg == 'cases':
                cases_start = time.time()

                print(" [x] Executing the cases task...")
                casesInformationProcess = ds_ParallelProcessing.caseProcess(1, 'DS_Case_Summary.txt')
                casesInformationProcess.start()
                self.publish(response, ch, method, properties, True)
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
                self.publish(response, ch, method, properties, True)
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
                self.publish(response, ch, method, properties, True)
                inventoryInformationProcess.join()

                inventory_end = time.time() - inventory_start 
                f = open('Inventory_Time.txt', 'a+')
                f.write(str(inventory_end) + '\n')
                f.close()

                print(" [.] Succeeded in processing the inventory task...")

        except Exception as e:

            response = str(e)
            self.publish(response, ch, method, properties, False)

    def publish(self, response, ch, method, properties, response_type = True):
            
        ch.basic_publish(exchange=self.server.exchange,
                            routing_key=properties.reply_to,
                            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                            body=str(response))
        
        if response_type:
            ch.basic_ack(delivery_tag=method.delivery_tag) 
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)
 
    def startServer(self):
        self._channel.basic_qos(prefetch_count=3)
        self._channel.basic_consume(self.server.queue, on_message_callback=self.callback)
        print('[*] Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()

if __name__ == '__main__':


    rKey = (sys.argv[1:])[0]
    queue = ''.join(e for e in rKey if e.isalnum()) + '_queue'
    #print('Routing key: {}'.format(rKey))

    serverConfig = RabbitMqServerConfigure(host= '192.168.0.148', 
                                           port= 5672,
                                           username= 'rabbituser', 
                                           password= 'rabbit1234', 
                                           queue= queue,
                                           routingKey=rKey)
    #serverConfig = RabbitMqServerConfigure(routingKey=rKey, queue=queue)
    messageQueueServer = RabbitMqServer(serverConfig)
    messageQueueServer.startServer()