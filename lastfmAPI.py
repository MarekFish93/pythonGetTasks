# Code here is not made by me. I only rewrite it for exercises purpose.
# Source of code: https://www.dataquest.io/blog/last-fm-api-python/
import requests
import json
import requests_cache
import time
from IPython.core.display import clear_output
import pandas as pd


API_KEY = '724bd376bad5bddf5f9b849997ea29ae'


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'rybulek90'}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


def jpprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


responses = []

page = 1
total_pages = 99999  # this is just a dummy number so the loop starts

# while loops generates above 6100 request so we need to use cache here
requests_cache.install_cache()
while page <= total_pages:
    payload = {
        'method': 'chart.gettopartists',
        'limit': 500,
        'page': page
    }

    # print some output so we can see the status
    print("Requesting page {}/{}".format(page, total_pages))
    # clear the output to make things neater
    clear_output(wait=True)

    # make the API call
    response = lastfm_get(payload)

    # if we get an error, print the response and halt the loop
    if response.status_code != 200:
        print(response.text)
        break

    # extract pagination info
    page = int(response.json()['artists']['@attr']['page'])
    total_pages = int(response.json()['artists']['@attr']['totalPages'])

    # append response
    responses.append(response)

    # if it's not a cached result, sleep
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)

    # increment the page number
    page += 1

# some data tidying
r0 = responses[0]
r0_json = r0.json()
r0_artists = r0_json['artists']['artist']
r0_df = pd.DataFrame(r0_artists)
r0_df.head()

frames = [pd.DataFrame(r.json()['artists']['artist']) for r in responses]
artists = pd.concat(frames)
artists.head()

artists = artists.drop('image', axis=1)

artists = artists.drop_duplicates().reset_index(drop=True)

artists.describe()
artists.head()


# using second method - artist.getTopTags

def lookup_tags(artist):
    r = lastfm_get({
        'method': 'artist.getTopTags',
        'artist': artist
    })

    # if there's an error, just return nothing
    if r.status_code != 200:
        return None

    # extract the top three tags and turn them into a string
    tags = [t['name'] for t in r.json()['toptags']['tag'][:3]]
    tags_str = ', '.join(tags)

    # rate limiting
    if not getattr(r, 'from_cache', False):
        time.sleep(0.25)

    return tags_str

