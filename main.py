from bs4 import BeautifulSoup
import requests

url = "https://vk.com/"
response = requests.get(url)
print(response.text)
