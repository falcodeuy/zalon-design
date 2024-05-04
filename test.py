import requests
from bs4 import BeautifulSoup
import json


def get_instagram_followers(user):
    url = f"https://www.instagram.com/{user}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    data = soup.find_all("meta", attrs={"property": "og:description"})
    text = data[0].get("content").split()
    followers = text[0]
    return followers


# Replace 'instagram' with the username of the Instagram account you want to check
print(" aaaaaaa")
print(get_instagram_followers("zalon.app"))
