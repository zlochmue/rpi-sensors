import datetime
import time
import glob
import requests
import json

def get_sensor_temp():   
    device = glob.glob("/sys/bus/w1/devices/" + "28*")[0] + "/w1_slave"

    with open(device, "r") as f:
        lines = f.readlines()
        f.close()

        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = round(float(temp_string) / 1000.0, 2)
            temp = ((temp*9)/5) + 32
            temp = round(temp,2)

    return temp

def get_API_temp():
    curr = 'https://api.openweathermap.org/data/2.5/weather?lat=41.87&lon=-87.62&appid=84105f1604d031a12cbcee0084df2326&units=imperial'
    response = requests.get(curr)
    y = response.json()
    itera = json.dumps(y,indent=3)
    y = json.loads(itera)
    return float(y["main"]["temp"])

def main():
    counter = 0
    while True:
    # scans temp once every sec_between_scan seconds
        sec_between_scan = 900
        start_now = datetime.datetime.now()
        formatted_date = start_now.strftime('%Y-%m-%d %H:%M:%S')

        # Measuring temperatures

        apitemp = get_API_temp()
        temp = get_sensor_temp()
        # check if temp/humidity is above certain levels and then signal 

        # send temperature scan to dynamodb db
        url = "https://jx7a1ot8db.execute-api.us-east-2.amazonaws.com/Post"
        counter += 1
        json_data = {"id" : str(counter),
                    "time" : str(formatted_date),
                    "apitemp" : str(apitemp),
                    "temp" : str(temp)}
        response = requests.post(url, json = json_data)
        print(f"Scan: {counter}, {formatted_date}, {temp}, {apitemp}") 

        time.sleep(sec_between_scan- time.time() % sec_between_scan)
        
        

if __name__ == "__main__":
    main()
