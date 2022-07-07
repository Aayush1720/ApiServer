import os
import asyncio
from azure.servicebus.aio import ServiceBusClient
import time 
import pymysql
import json


CONNECTION_STR = "Endpoint=sb://mysql-aayush.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=NgV33DLGKSD5qRskYrL5Pu3qJVB7XebMnog/xIk3K9A="
QUEUE_NAME = "q1"

def db_connect():
	conn = pymysql.connect(host='ndep-aayush-mysql-poc.mysql.database.azure.com', port=3306, user='aayush1@ndep-aayush-mysql-poc', passwd='Aayush@123', db='test1', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	return conn


def update_mysql_status(id, status):
    print(id,status)
    conn = db_connect()
    cursor = conn.cursor()
    sql_string = "UPDATE Deployment SET cluster_status = %s WHERE id = %s"
    try:
        cursor.execute(sql_string, (status,id))
        conn.commit()
        conn.close()
        print("changed status of "+ str(id) +" to " + str(status) )
    except Exception as ex:
        print("exception ->")
        print(ex)


async def main():
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)

    async with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
        async with receiver:
            #received_msgs = await receiver.peek_messages(max_message_count=2)
            messages = await receiver.receive_messages()
            for msg in messages:
                print(str(msg))
                id = json.loads(str(msg)).get("id")
                time.sleep(2)
                ## bicep call maybe
                status="SUCCESSFUL"
                update_mysql_status(id,status)
                await receiver.complete_message(msg)

                ## logging the changes --  only for now -> testing purpose
                my_file = open("/home/nuance/dev/api_dev/node_api/reciever_log.txt", 'a')
                my_file.write("changes status of " + str(id) + " to " + str(status) + "\n")



asyncio.run(main())