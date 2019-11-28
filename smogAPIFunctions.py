import requests

# Taking whole list of station
basic_url = 'http://api.gios.gov.pl/pjp-api/rest/station/findAll'

# Url for positions
url_for_positions = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/'

# url for data from sensors
url_for_sensors_data = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/'

# Generator finding station by name using regex, returns id of stations
def find_station_by_name(word):
    stations = requests.get(basic_url)
    list_of_stations = stations.json()
    for i in list_of_stations:
        if word.search(i['stationName']):
            yield i['id']


# Generator finding position by stationID, returns id of positions
def find_position_by_stationID(word):
    for i in find_station_by_name(word):
        positions_raw = requests.get(url_for_positions + str(i))
        position = positions_raw.json()
        yield position


# Finding positions with PM10, PM2.5 and CO parameters
def find_positions_with_parameters(word):
    for i in find_position_by_stationID(word):
        for x in range(0, len(i)):
            if i[x]['param']['paramCode'] in ['PM10', 'PM2.5', 'CO']:
                yield i[x]['id']


def return_result(word):
    pm10 = [0, 0]
    pm25 = [0, 0]
    co = [0, 0]

    try:
        for i in find_positions_with_parameters(word):
            sensors_data_raw = requests.get(url_for_sensors_data + str(i))
            sensors_data = sensors_data_raw.json()

            if sensors_data['key'] == 'PM10':
                pm10[1] += 1
                if sensors_data['values'][0]['value'] is not None:
                    pm10[0] += sensors_data['values'][0]['value']
                else:
                    while True:
                        for x in range(1, 10):
                            if sensors_data['values'][x]['value'] is not None:
                                pm10[0] += sensors_data['values'][x]['value']
                                break
                        break

            elif sensors_data['key'] == 'PM2.5':
                pm25[1] += 1
                if sensors_data['values'][0]['value'] is not None:
                    pm25[0] += sensors_data['values'][0]['value']
                else:
                    while True:
                        for x in range(1, 10):
                            if sensors_data['values'][x]['value'] is not None:
                                pm25[0] += sensors_data['values'][x]['value']
                                break
                        break

            else:
                co[1] += 1
                if sensors_data['values'][0]['value'] is not None:
                    co[0] += sensors_data['values'][0]['value']
                else:
                    while True:
                        for x in range(1, 10):
                            if sensors_data['values'][x]['value'] is not None:
                                co[0] += sensors_data['values'][x]['value']
                                break
                        break
        print(f'Średnie PM10 w twoim mieście wynosi {pm10[0] / pm10[1]}')
        print(f'Średnie PM25 w twoim mieście wynosi {pm25[0] / pm25[1]}')
        print(f'Średnie CO w twoim mieście {co[0] / co[1]}')
    except:
        print('Your city has no sensors')
