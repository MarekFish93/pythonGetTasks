# Code from this module is not orginally made by me. I only rewrite it for excersises purpose.
# Source of code: https://medium.com/quick-code/absolute-beginners-guide-to-slaying-apis-using-python-7b380dc82236

import requests

# Specify parameter
parameter = {"rel_rhy":"jingle"}

# Bild a whole GET request
request = requests.get('https://api.datamuse.com/words',parameter)

# Cast JSON to dictionary
rhyme_jingle = request.json()

# Loop through dictionary to print 10 rhymes
for rhyme in rhyme_jingle[0:10]:
    print(rhyme['word'])