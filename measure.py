import os
import glob
import requests
import json

def get_sensor_temp():
    
    device = glob.glob("/sys/bus/w1/devices/" + "28*")[0] + "/w1_slave"

    with open(device, "r") as f:
        lines = f.readlines()
        
    while lines[0].strip()[-3:] != "YES":
        lines = read_temp_raw()
    
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp = round(float(temp_string) / 1000.0, 2)
        temp = ((temp*9)/5) + 32
        temp = round(temp,2)

    return temp


# return the current temperature in Chicago from weather API
def get_API_temp():
	curr = 'https://api.openweathermap.org/data/2.5/weather?lat=41.87&lon=-87.62&appid=84105f1604d031a12cbcee0084df2326&units=imperial'
	response = requests.get(curr)
	y = response.json()
	itera = json.dumps(y,indent=3)
	y = json.loads(itera)
	return float(y["main"]["temp"])
        
if __name__ == "__main__":
    print(get_sensor_temp())    
