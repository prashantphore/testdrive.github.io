import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",password="",database="firstwebsite")

if mydb.is_connected():
    print("successful connected")