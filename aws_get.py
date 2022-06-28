import aws_dyna
from dynamodb_json import json_util as json
import pandas as pd
import matplotlib.pyplot as plt


def main():
    obj = aws_dyna.DB("temps")
    #obj.get(... ) to give me all data
    lst = obj.get_all
    obj = pd.DataFrame(json.loads(lst))
    print(f"Table fetched\n {obj}")
    
    obj= obj.sort_values(by=['timestamp'])
    print(f"Sorted table\n {obj}")
    obj['temp'] = obj['temp'].astype(float)
    obj['api-temp'] = obj['api-temp'].astype(float)
    obj.plot(x='timestamp', y = 'temp')
    print("plotting")
    plt.savefig('plot.png')

    obj.plot(x='timestamp', y = 'api-temp')
    plt.savefig('api-plot.png')


if __name__ == "__main__":
    main()
