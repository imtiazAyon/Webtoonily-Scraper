import re
import time
import os
import shutil
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import cloudscraper

link = input("Enter chapter link:")
s = cloudscraper.CloudScraper()
i = 0
while True:
	cookies = s.get(link).cookies 
	headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0', 'Referer':link}
	response = requests.get(link)
	soup = BeautifulSoup(response.text, "html.parser")
	chapter =soup.find("h1", {"id": "chapter-heading"}).getText()
	path = "images/"+chapter+"/"
	if not os.path.exists(path):
		os.makedirs(path)
	elems =soup.find_all("div", {"class": "reading-content"})[0]
	img_elems = elems.find_all('img')
	img = [img_elem.attrs['src'] for img_elem in img_elems]
	img = list(dict.fromkeys(img))
	loop = len(img)
	num = 1
	for i in range(loop):
		file_path = Path(path + str(num).zfill(2) + ".png")
		R = s.get(img[i],headers=headers, cookies=cookies, allow_redirects=True)
		if R.status_code != 200:
			print("Error: "+img[i])
		#time.sleep(1)
		file_path.write_bytes(R.content)
		print(f"Downloaded page {num}...", end='\r')
		num = num + 1
	print(f"Downloaded {chapter}...", end='\r')
	i = i + 1
	elems =soup.find_all("a", {"class": "btn next_page"})
	if elems==[]:
		break
	link = elems[0].attrs['href']
print(f"Done!")