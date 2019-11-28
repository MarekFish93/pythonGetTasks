# Code from this module is not orginally made by me. I only rewrite it for excersises purpose.
# Source of code: https://medium.com/quick-code/absolute-beginners-guide-to-slaying-apis-using-python-7b380dc82236

import requests

# Taking a data from NAS Open API
request = requests.get('http://api.open-notify.org/astros.json')

# Casting json data to dictionary
people = request.json()

# Printing astronauts beeing currently in space
# for i in people['people']:
#     print(i['name'])

# Getting number of people in space

people_in_space = people['number']
