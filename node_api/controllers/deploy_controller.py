import connexion
import json
import pymysql
import uuid
from datetime import datetime
#from dev.api_dev.node_api.test_sb import send_single_message
from .. import messages
from azure.servicebus import ServiceBusClient, ServiceBusMessage


CONNECTION_STR = "Endpoint=sb://mysql-aayush.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=NgV33DLGKSD5qRskYrL5Pu3qJVB7XebMnog/xIk3K9A="
QUEUE_NAME = "q1"

def send_single_message(sender, message):
	message = ServiceBusMessage(message)
	print(message)
	sender.send_messages(message)
	print("sent message")


def db_connect():
	conn = pymysql.connect(host='ndep-aayush-mysql-poc.mysql.database.azure.com', port=3306, user='aayush1@ndep-aayush-mysql-poc', passwd='Aayush@123', db='test1', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	return conn


def get_serialized_deployments(cursor):
	res = []
	for row in cursor:
		res += [row]
	res = json.dumps(res, sort_keys=False,indent = 4, separators=(',',': '))
	print(res)
	return res

def get_deployments():
	print("in get deployments function")
	# sql query
	conn = db_connect()
	cursor = conn.cursor()
	cursor.execute("Select * from Deployment")
	res = get_serialized_deployments(cursor)
	conn.close()
	return res
	
def make_Deployment(body):
	# getting all the fields from body
	cluster_name = body.get("cluster_name")
	resource_group = body.get("resource_group")
	region = body.get("region")
	node_size = body.get("node_size")
	node_count = body.get("node_count")

	# generating id and getting current time
	id = str(uuid.uuid1())
	print(id)
	now = datetime.now()
	now = str(now.strftime("%m/%d/%Y, %H:%M:%S"))
	# right now no exception handling or checking if req value is provided or not
	# addeing above info to DB
	conn = db_connect()
	cursor = conn.cursor()
	print(now)
	sql_string = "INSERT INTO Deployment (`id`, `cluster_name`, `cluster_status`, `created_at`, `resource_group`, `region`, `node_size`, `node_count` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )"
	try:
		cursor.execute(sql_string, (id, cluster_name, "PENDING",now , resource_group, region, node_size, node_count))
		conn.commit()
	except Exception as ex:
		print("exception -> ")
		print(ex)
	conn.close()
	# sending the message in the queue
	message  = {
		"id"             : id,
		"cluster_name"   : cluster_name,
		"resource_group" : resource_group,
		"region"         : region,
		"node_size"      : node_size,
		"node_count"     : node_count
	}
	message = json.dumps(message) ## converting to string
	
	servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

	with servicebus_client:
		sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
		with sender:
			send_single_message(sender, message)

	return id










def test1(fname= "defaul_first", lname="default_second"):
        print("in test 1")
        return fname + " " + lname

def test2():
        return "bla"