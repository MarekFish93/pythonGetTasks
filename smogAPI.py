# Simple program returning mean PM10 and PM2.5 from every station in city from input.
# Connected to gios.gov.pl data
# Works only for polish cities
import requests
import re

# All functions are in smogAPIFunctions.py
from smogAPIFunctions import return_result

# Taking


word = re.compile(input('What polish city you want to check?'))

return_result(word)
