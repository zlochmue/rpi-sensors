import requests
import json

# return the current temperature in Chicago from weather API
def get_current_temp():
	curr = 'https://api.openweathermap.org/data/2.5/weather?lat=41.87&lon=-87.62&appid=84105f1604d031a12cbcee0084df2326&units=imperial'
	response = requests.get(curr)
	y = response.json()
	itera = json.dumps(y,indent=3)
	y = json.loads(itera)
	return float(y["main"]["temp"])
