from bs4 import BeautifulSoup
import requests
import re
BASE_URL = 'https://api.genius.com'
class lyrics:
    def __init__(self, artist, title, access_token, remove_section_headers=True):
        self.artist = artist
        self.title = title
        self.token = access_token
        self.remove_section_headers = remove_section_headers
    def _get_song_details(self):
        details = None
        try:
            headers = {'Authorization': 'Bearer ' + self.token}
            data = {'q': self.title + ' ' + self.artist}
            response = requests.get('{}/search'.format(BASE_URL), data=data, headers=headers).json()
            for hit in response['response']['hits']:
                if self.artist.lower() in hit['result']['primary_artist']['name'].lower():
                    details = hit
                    break
        except requests.exceptions.RequestException:
            pass
        return details
    def extract_lyrics(self):
        lyrics = 'Текст не найден!'
        data = self._get_song_details()
        if data:
            url = data['result']['url']
            page = requests.get(url)
            html = BeautifulSoup(page.text, 'html.parser')
            lyrics = html.find('div', class_='lyrics')
            if lyrics is not None:
                lyrics = lyrics.get_text().strip()
        #Убирает [Текст песни ""], [Припев], [Куплет 1,2,3]
        if self.remove_section_headers:
            lyrics = re.sub('(\\[.*?\\])*', '', str(lyrics))
            lyrics = re.sub('\n{2}', '\n', str(lyrics))
        return lyrics.strip("\n") 



