# get images(JPG/JPEG/PNG) from a webpage and save them to a folder
# 可以正常抓取的网站：Moondroplab.com下的各种page
# Author: Inori-333
# Update: 2025/02/05
# License: Apache License 2.0

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_images(url, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags and background images in 'a' tags
    img_tags = soup.find_all('img')
    bg_img_tags = soup.find_all('a', style=True)

    # Download each image
    for img in img_tags:
        img_url = img.get('src')
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

    # Download each background image
    for bg_img in bg_img_tags:  # 遍历所有带有背景图片的'a'标签
        style = bg_img.get('style')  # 获取'a'标签的style属性
        if 'background-image' not in style:  # 如果style属性中不包含背景图片，则跳过
            continue
        start = style.find('url(') + 4  # 找到背景图片URL的起始位置
        end = style.find(')', start)  # 找到背景图片URL的结束位置
        bg_img_url = style[start:end].strip('"\'')  # 提取并清理背景图片URL
        bg_img_url = urljoin(url, bg_img_url)  # 将相对URL转换为绝对URL
        bg_img_name = os.path.basename(bg_img_url)  # 获取背景图片的文件名

        # Check if the image is in JPG/JPEG/PNG format
        # 检查图片格式是否为JPG/JPEG/PNG
        if not bg_img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        bg_img_path = os.path.join(output_folder, bg_img_name)  # 构建图片保存路径

        # Download and save the image
        bg_img_data = requests.get(bg_img_url).content  # 下载背景图片内容
        with open(bg_img_path, 'wb') as f:  # 以二进制写入方式打开文件
            f.write(bg_img_data)  # 将图片内容写入文件
        print(f'Downloaded {bg_img_url} to {bg_img_path}')  # 打印下载成功信息


if __name__ == '__main__':
    url = "https://moondroplab.com/cn/drawing?83217ef8_page=2"
    output_folder = "E://Inori_Code//Python//Image_output"
    download_images(url, output_folder)
