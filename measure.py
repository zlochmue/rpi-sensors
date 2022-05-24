import os
import glob

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
        
        
if __name__ == "__main__":
    print(get_sensor_temp())    