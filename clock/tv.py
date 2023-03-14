import datetime
import requests
import json
import os

class Sonarr:

    def __init__(self):
        self._url = os.environ['SONARR_URL']
        self._token = os.environ['SONARR_TOKEN']

    def get_calendar(self):
        today = datetime.date.today()

        headers =  {"X-Api-Key": self._token}
        params = {
            'start': (today + datetime.timedelta(days=-1)), 
            'end': (today + datetime.timedelta(days=14)),
            'includeSeries': 'true'
        }
        response = requests.get(f"{self._url}/api/v3/calendar", params=params, headers=headers)
        calendar = response.json()
        return calendar

if __name__ == '__main__':
    sonarr = Sonarr()
    calendar = sonarr.get_calendar()
    print(calendar)



# for episode in calendar:
#     air_date = datetime.datetime.strptime(episode['airDate'], '%Y-%m-%d')
#     if air_date.date() < today:
#         print(f"before ", end='')
#     elif air_date.date() < (today + datetime.timedelta(days=1)):
#         print(f"TODAY! ", end='')
#     elif air_date.date() < (today + datetime.timedelta(days=2)):
#         print(f"Tomorrow! ", end='')
#     elif air_date.date() < (today + datetime.timedelta(days=7)):
#         print(f"{air_date.strftime('%A')} ", end='')
#     else:
#         print(f"{air_date.date()} ", end='')

#     print(f"{episode['series']['title']} ", end='')
#     print(f"- S{episode['seasonNumber']}E{episode['episodeNumber']} ", end='')
#     print(f"- {episode['title']}")
