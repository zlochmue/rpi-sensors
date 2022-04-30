import os
import mariadb as db
import time
from datetime import datetime
import random

start_time = time.time()
start_now = datetime.now()
while True:
    # scans once every sec_between_scan seconds 
    sec_between_scan = 30
    time.sleep(sec_between_scan- time.time() % sec_between_scan)
    print("Connecting to Database...")
    start_now = datetime.now()
    formatted_date = start_now.strftime('%Y-%m-%d %H:%M:%S')
    username = os.environ.get("username")
    password = os.environ.get("password")

    conn = db.connect(user='zeek',
                password= 'XXXXXX',
                host= "localhost",
                database= "temps")

    cur = conn.cursor()

    # takes measurement and inserts into the database
    print("Measuring temperature...")
    sql= "INSERT INTO temps (entry, temp1, temp2) VALUES (?,?,?)"
    rand1= random.randint(0,100) # change to temp sensor take
    rand2= random.randint(0,100) # change to temp sensor take
    data= (formatted_date, rand1, rand2)
    print("Sending data...")
    cur.execute(sql, data)

    conn.commit()

    cur.close()
    conn.close()
