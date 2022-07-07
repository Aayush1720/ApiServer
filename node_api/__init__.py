#from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL
import connexion
import json
import pymysql


#db = SQLAlchemy()

# connecting top open api via connexion
app = connexion.App(__name__, specification_dir='openapi/')  # AioHttp
app.add_api('openapi.yaml', arguments={'title': 'NDEP ODE API'}, pythonic_params=True)


"""
conn = pymysql.connect(host='ndep-aayush-mysql-poc.mysql.database.azure.com', port=3306, user='aayush1@ndep-aayush-mysql-poc', passwd='Aayush@123', db='test1', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
"""
