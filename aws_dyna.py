import datetime
import time
import boto3
from measure import get_sensor_temp, get_API_temp

class DB(object):

    def __init__(self, name='temps'):
        self.name=name
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(name)
        self.client = boto3.client('dynamodb')

    @property
    def get_all(self):
        """response = self.table.get_item(
            Key=
            {
                'id':"1"
            }
        )"""
        response = self.table.scan()
        items = response['Items']

        return list(items)

    def put(self, id='' , temp='',atemp='',stamp=''):
        self.table.put_item(
            Item={
                'id':id,
                'temp':temp,
                'api-temp':atemp,
                'timestamp':stamp
            }
        )

    def delete(self,id=''):
        self.table.delete_item(Key={'id': id})

    def describe_table(self):
        response = self.client.describe_table(TableName='temps')
        return response

def main():
    counter = 0
    print("Starting...")
    while True:
    # scans temp about once every sec_between_scan seconds
        sec_between_scan = 1
        time.sleep(sec_between_scan- time.time() % sec_between_scan)
        # Connecting to Database
        obj = DB()

        start_now = datetime.datetime.now()
        formatted_date = start_now.strftime('%Y-%m-%d %H:%M:%S')

        # Measuring temperatures

        apitemp = get_API_temp()
        temp = get_sensor_temp()

        # Sending data to DB
        obj.put(id=str(counter), temp=str(temp), atemp=str(apitemp),stamp=str(formatted_date))
        print(f"Scan: {counter}, {formatted_date}, {temp}, {apitemp}") 
        counter += 1
        

if __name__ == "__main__":
    main()
