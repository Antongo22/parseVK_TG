from bs4 import BeautifulSoup
import requests

url = "https://web.telegram.org/k/"
response = requests.get(url)
print(response.text)
new_name = "tg"


class Parser:
    pass
