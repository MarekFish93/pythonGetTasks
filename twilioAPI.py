# Code from this module is not orginally made by me. I only rewrite it for excersises purpose.
# Source of code: https://medium.com/quick-code/absolute-beginners-guide-to-slaying-apis-using-python-7b380dc82236

import requests
from twilio.rest import Client
from nasaAPI import people_in_space

# My phone number iso2022_jp +18058745264

# Creating variables with authorization data
account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'

client = Client(account_sid, auth_token)

# Creating a message with info about people in space taken from nasaAPI module

message = 'Hi. Did u know that currently NASA has like '+str(people_in_space)+' people in space?'

# Sending message

message_to_send = client.messages.create(
    to = 'xxxxxxxxxx',
    from_= '+18058745264',
    body = message)
