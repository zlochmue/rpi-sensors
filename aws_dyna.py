import datetime
import time
import glob
import requests
import json

class RPIwrapper:

    def run(self, sec_per_scan, postURL, weatherURL):
        scanID = 0
        while True:
            apitemp = self.get_API_temp(weatherURL)
            temp = self.read_sensor_temp()

            response = self.post_temp_scan(scanID, postURL, temp, apitemp)
            # add notifications/logging using response

            scanID += 1
            time.sleep(sec_per_scan - time.time() % sec_per_scan)

    @staticmethod
    def read_sensor_temp():   
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

    @staticmethod
    def get_API_temp(url):
        response = requests.get(url)
        y = response.json()
        itera = json.dumps(y,indent=3)
        y = json.loads(itera)
        return float(y["main"]["temp"])

    @staticmethod
    def post_temp_scan(id, url, temp, apitemp):
        start_now = datetime.datetime.now()
        formatted_date = start_now.strftime('%Y-%m-%d %H:%M:%S')
        
        json_data = {"id" : str(id),
                    "time" : str(formatted_date),
                    "apitemp" : str(apitemp),
                    "temp" : str(temp)}

        print(f"Scan: {id}, {formatted_date}, {temp}, {apitemp}") 

        return requests.post(url, json = json_data)

def main():
        RPI = RPIwrapper()

        weatherURL = "https://api.openweathermap.org/data/2.5/weather?lat=41.87&lon=-87.62&appid=84105f1604d031a12cbcee0084df2326&units=imperial"
        postURL = "https://jx7a1ot8db.execute-api.us-east-2.amazonaws.com/Post"
        sec_per_scan = 900
        
        RPI.run(sec_per_scan, postURL, weatherURL)
        
        
if __name__ == "__main__":
    main()
