from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import asyncio
from azure.servicebus.aio import ServiceBusClient


CONNECTION_STR = "Endpoint=sb://mysql-aayush.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=NgV33DLGKSD5qRskYrL5Pu3qJVB7XebMnog/xIk3K9A="
QUEUE_NAME = "q1"


def send_single_message(message):
    

    message = ServiceBusMessage('{ "name" : "aayush" }')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    
    with servicebus_client:
        print("hello")
        # sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        # with sender:
        #     sender.send_messages(message)
        #     print("Sent a single message")

    