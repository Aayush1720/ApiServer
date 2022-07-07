from azure.servicebus import ServiceBusClient, ServiceBusMessage

import os
CONNECTION_STR = "Endpoint=sb://mysql-aayush.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=NgV33DLGKSD5qRskYrL5Pu3qJVB7XebMnog/xIk3K9A="
QUEUE_NAME = "q1"


def send_single_message(sender):
    message = ServiceBusMessage('{ "name" : "aayush" }')
    sender.send_messages(message)
    print("Sent a single message")


servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
    with sender:
        send_single_message(sender)