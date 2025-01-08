import requests
from bs4 import BeautifulSoup
import os


def fetch_soul_images():
    url = "https://onmyoji.fandom.com/wiki/Soul/List#Released"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    directory = "./img"
    # Create a directory to store downloaded files
    os.makedirs(directory, exist_ok=True)
    for img_tag in soup.select('td a[href]'):
        soul_url = "https://onmyoji.fandom.com/" + img_tag['href']
        # img_url = img_tag['src'].split('/revision')[0]
        filename = soul_url.split('/')[-1]
        res2 = requests.get(soul_url)

        # # Download image
        # img_data = requests.get(img_url).content
        #
        # # Clean filename
        # filename = f"{title.replace(' ', '_')}.png"

        soup_ = BeautifulSoup(res2.content, 'html.parser')

        img_urls = []
        for img in soup_.select('div.center img'):
            if img.get('src'):
                img_urls.append(img['src'])

        # Download images
        for i, url in enumerate(img_urls):
            try:
                img_data = requests.get(url).content
                with open(f"{directory}/{filename}.png", 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                print(f"Failed to download {url}: {e}")


if __name__ == "__main__":
    fetch_soul_images()

