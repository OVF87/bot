from config import appid
import requests


def get_city_id(s_city_name):
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    print(data)
    if data['list']:
        city_id = data['list'][0]['id']
        print(city_id)

        return city_id
    else:
        data['list'][0]['id'] = 0
        print(data)
        city_id = data['list'][0]['id']
        print(city_id)
        return city_id


def get_wind_direction(deg):
    res = []
    direction = ['Северный', 'Северо-восточный', ' Восточный', 'Юго-восточный ', 'Южный',
                 'Юго-запвдный', 'Западный', 'Северо-западный']
    for i in range(0, 8):
        step = 45.
        min_sector = i * step - 45 / 2.
        max_sector = i * step + 45 / 2.
        if i == 0 and deg > 360 - 45 / 2.:
            deg = deg - 360
        if min_sector <= deg <= max_sector:
            res = direction[i]
            break
    return res


def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        answer = dict()
        answer['Сейчас'] = " Условия: " + str(data['weather'][0]['description']) + '\n' + \
                           " Температура: " + str(data['main']['temp']) + ' C' + '\n' + \
                           " Ощущается: " + str(data['main']['feels_like']) + ' C' + '\n' + \
                           " Ветер: " + str(data['wind']['speed']) + ' м/с' + '\n' + \
                           " Направление: " + str(get_wind_direction(data['wind']['deg']))
        return answer
    except Exception as e:
        print("Exception (weather):", e)
        pass


def request_forecast(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        answer = dict()
        answer['Город'] = (data['city']['name'] + ' ' + data['city']['country'])
        for i in range(2, len(data['list']), 4):
            answer[data['list'][i]['dt_txt']] = '\n' +  \
                " Условия: " + str(data['list'][i]['weather'][0]['description']) + '\n' + \
                " Температура: " + str(data['list'][i]['main']['temp']) + ' C' + '\n' + \
                " Ощущается: " + str(data['list'][i]['main']['feels_like']) + ' C' + '\n' + \
                " Ветер: " + str(data['list'][i]['wind']['speed']) + " м/с" + '\n' + \
                " Направление: " + str(get_wind_direction(data['list'][i]['wind']['deg']))
        return answer
    except Exception as e:
        print("Exception (forecast):", e)
        pass
