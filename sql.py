import os
import mariadb as db
import time
from datetime import datetime
from random import randint
from weath import get_current_temp
from measure import get_sensor_temp

start_time = time.time()
start_now = datetime.now()
username = os.environ.get("username")
password = os.environ.get("password")

while True:
    # scans temp once every sec_between_scan seconds
    sec_between_scan = 300
    time.sleep(sec_between_scan- time.time() % sec_between_scan)
    # Connecting to Database
    start_now = datetime.now()
    formatted_date = start_now.strftime('%Y-%m-%d %H:%M:%S')

    conn = db.connect(user=username,
                password=password,
                host= "127.0.0.1",
                database= "temps")

    cur = conn.cursor()

    # Measuring temperature

    curr = get_current_temp()
    temp = get_sensor_temp()

    data= (formatted_date, temp, curr)

    # Sending data
    sql= "INSERT INTO measurements (time, temp, curr_temp) VALUES (?,?,?)"
    cur.execute(sql, data)

    conn.commit()
    
    print(f"Scan: {formatted_date}, {temp}, {curr}") 

    cur.close()
    conn.close()
