import datetime
import logging
import json
import os
import requests
from display.canvas import Canvas

logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.WARNING)

class Tv:

    def __init__(self, size):
        self._size = size
        self._url = None
        self._token = None
        if 'SONARR_URL' in os.environ:
            self._url = os.environ['SONARR_URL']
        if 'SONARR_TOKEN' in os.environ:
            self._token = os.environ['SONARR_TOKEN']
        self._canvas = Canvas(size, "origin_tech", 300)
        self._last_update = datetime.datetime(1977, 4, 20)
        self._next_update = datetime.datetime(1977, 4, 20)
        self._calendar_data = None

    def get_canvas(self) -> Canvas:
        """Returns the currently-drawn Canvas

        Returns:
            Canvas: the Canvas object
        """
        return self._canvas

    def tick(self) -> bool:
        now = datetime.datetime.now()

        if self._last_update < (now - datetime.timedelta(hours=3)):
            logger.info("Data refresh required")
            self._calendar_data = self.get_calendar()
            self.render()
            return True

        return False

    def get_calendar(self):
        logger.info("Refreshing TV calendar data")
        today = datetime.date.today()

        headers = {"X-Api-Key": self._token}
        params = {
            'start': (today + datetime.timedelta(days=-1)), 
            'end': (today + datetime.timedelta(days=14)),
            'includeSeries': 'true'
        }
        response = requests.get(f"{self._url}/api/v3/calendar",
                                params=params,
                                headers=headers,
                                timeout=30)
        calendar = response.json()
        logger.info("Got %s episodes", len(calendar))
        self._last_update = datetime.datetime.now()
        return calendar
    
    def render(self):
        logger.info("Rendering data")
        logger.info(self._calendar_data)
        self._canvas.blank()

        max_rows = 2
        row_height = self._size[1]//max_rows
        rows = min(max_rows, len(self._calendar_data))

        for i in range(0, rows):
            episode = self._calendar_data[i]
            text = f"S{episode['seasonNumber']}E{episode['episodeNumber']} {episode['series']['title']}"
            pos = (i+1)*row_height
            logger.info("Episode %s %s", text, pos)
            sprite = self._canvas.create_text_object(text, height=row_height)
            self._canvas.place_sprite(sprite, (0, pos), "bottom")

if __name__ == '__main__':
    sonarr = Tv((800,600))
    c = sonarr.get_calendar()
    print(c)



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
