import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_images(url, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the webpage content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img', {'class': 'mimg'})

    # Download each image
    for img in img_tags:
        img_url = img.get('src') or img.get('data-src')
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        img_name = os.path.basename(img_url)

        # Check if the image is in JPG/JPEG/PNG format
        if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img_path = os.path.join(output_folder, img_name)

        # Download and save the image
        img_data = requests.get(img_url).content
        with open(img_path, 'wb') as f:
            f.write(img_data)
        print(f'Downloaded {img_url} to {img_path}')


if __name__ == '__main__':
    url = "https://www.bing.com/images/search?q=miku+fufu&qpvt=miku+fufu&form=IGRE&first=1"
    output_folder = "E://Inori_Code//Python//Image_output"
    download_images(url, output_folder)
