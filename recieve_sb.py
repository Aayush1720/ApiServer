from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json

CONNECTION_STR = "Endpoint=sb://mysql-aayush.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=NgV33DLGKSD5qRskYrL5Pu3qJVB7XebMnog/xIk3K9A="
QUEUE_NAME = "q1"

servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5)
    with receiver:
        for msg in receiver:
            print("Received: ")
            st = str(msg)
            mes = json.loads(st)
            print(mes)

            receiver.complete_message(msg)