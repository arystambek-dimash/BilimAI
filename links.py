import requests
from bs4 import BeautifulSoup
from googlesearch import search
import certifi


def get_link(question):
    search_results = search(question, tld="co.in", num=10, stop=10, pause=2)
    valid_links = []

    for link in search_results:
        try:
            response = requests.get(link, verify=certifi.where())
            if response.status_code == 200:
                valid_links.append(link)
        except requests.exceptions.SSLError as e:
           pass

    return valid_links[:3]


