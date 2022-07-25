import datetime
import time
import boto3
import glob
import requests
import json

class DB(object):

    def __init__(self, name='sensor'):
        self.name=name
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(name)
        self.client = boto3.client('dynamodb')

    @property
    def get_all(self):
        response = self.table.scan()
        items = response['Items']
        return list(items)

    def put(self, id='' , temp='',atemp='',stamp=''):
        self.table.put_item(
            Item={
                'id':int(id),
                'time':stamp,
                'apitemp':atemp,
                'temp':temp,
            }
        )

    def delete(self,id=''):
        self.table.delete_item(Key={'id': id})

    def describe_table(self):
        response = self.client.describe_table(TableName='sensor')
        return response

    def get_sensor_temp(self):   
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

    def get_API_temp(self):
        curr = 'https://api.openweathermap.org/data/2.5/weather?lat=41.87&lon=-87.62&appid=84105f1604d031a12cbcee0084df2326&units=imperial'
        response = requests.get(curr)
        y = response.json()
        itera = json.dumps(y,indent=3)
        y = json.loads(itera)
        return float(y["main"]["temp"])

def main():
    counter = 0
    while True:
    # scans temp about once every sec_between_scan seconds
        sec_between_scan = 450
        time.sleep(sec_between_scan- time.time() % sec_between_scan)
        # Connecting to Database
        obj = DB()

        start_now = datetime.datetime.now()
        formatted_date = start_now.strftime('%Y-%m-%d %H:%M:%S')

        # Measuring temperatures

        apitemp = obj.get_API_temp()
        temp = obj.get_sensor_temp()

        # PUT data to DB
        counter += 1
        obj.put(id=str(counter), temp=str(temp), atemp=str(apitemp),stamp=str(formatted_date))
        print(f"Scan: {counter}, {formatted_date}, {temp}, {apitemp}") 
        
        

if __name__ == "__main__":
    main()
