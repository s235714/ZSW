from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import urllib
import urllib.request
import os, os.path
import random

html = urlopen('https://www.flickr.com/search/?q=flowers')
bs = BeautifulSoup(html, 'html.parser')

#print(str(bs))

images = re.findall("[a-z \- A-Z 0-9 \. ]+\.com[a-z \- A-Z 0-9 \. \/ \_ \-]+\.jpg", str(bs))

print(str(images))

licznik = 1


for image in images:
    urllib.request.urlretrieve('https://'+str(image), 'img'+str(licznik)+'.jpg')
    print('pyk')
    licznik = licznik + 1

print('pobrano')
licznik-=1
list = os.listdir(r"C:\Users\michal_internet\Desktop\Pythony\Kwiatki")

#print(str(list))

list.remove('obraz.py')
print(str(list))

wybor = random.randrange(1, 25)
print(str(wybor))

file_name = list[wybor]

from PIL import Image, ImageFilter, ImageFont, ImageDraw
import PIL
import datetime
from datetime import time, date
import textwrap


im = Image.open(file_name)
x, y = im.size
print(str(x)+"x"+str(y))

mnoznik = 2
new_x =x*mnoznik
new_y =y*mnoznik
print(str(new_x)+"x"+str(new_y))
im = im.resize((new_x, new_y), PIL.Image.NEAREST)

im = im.filter(ImageFilter.GaussianBlur(4))

data = date.today()
godzina = time()

print(str(data))
print(str(godzina))

dni_tygodnia = {"poniedzialek", "wtorek", "srode", "czwartek", "piatek", "sobote", "niedziele"}


pixels = im.load()

for i in range(im.size[0]):
    for j in range(im.size[1]):
       r, g, b = pixels[i, j]
       r+=60
       g+=60
       b+=60
       if(r>255):
           r = 255
       if (b > 255):
           b = 255
       if (g > 255):
           g = 255
       pixels[i, j] = (r, g, b)


color = (0, 0, 255)


fnt = ImageFont.truetype('C:\Windows\WinSxS\amd64_microsoft-windows-f..ruetype-comicsansms_31bf3856ad364e35_10.0.17763.1_none_cd1b0da8928bffc1\comic.ttf', 40)

d = ImageDraw.Draw(im)

row1 = "WITAMY"
row2 = "SERDECZNIE"

w1, h1 = d.textsize(row1, font=fnt)
w2, h2 = d.textsize(row2, font=fnt)

print(str(w1))
print(str(w2))

print(str(new_x))


d.text(((new_x/2) - (w1/2), (new_y/2-h1)), row1, font=fnt, fill=color)
d.text(((new_x/2) - (w2/2), (new_y/2+h1)), row2, font=fnt, fill=color)

off1 = 60
off2 = 150

kolor_tla = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))

img = Image.new('RGB', (new_x, off2), color=kolor_tla)

img1 = Image.new('RGB', (new_x, off1), color=kolor_tla)

total_width = new_x
max_height = new_y+off1+off2

new_im = Image.new('RGB', (total_width, max_height))

images = [img1, im, img]

x_offset = 0
for i in images:
    new_im.paste(i, (0, x_offset))
    x_offset += i.size[1]

temp = 22 ######beda brane jako argumenty #soon
wilgonosc = 15
halas = "cicho"

kolor_font = (255-kolor_tla[0], 255-kolor_tla[1], 255-kolor_tla[2])

d1 = ImageDraw.Draw(new_im)
d1.text((10, off1+new_y), "temperatura: "+str(temp)+"°C", font=fnt, fill=kolor_font)
d1.text((10, off1+new_y+45), "wilgotnosc: "+ str(wilgonosc)+"%", font=fnt, fill=kolor_font)
d1.text((10, off1+new_y+90), "halas: " + halas, font=fnt, fill=kolor_font)
d1.text((10, 0), "Dzis jest: "+str(datetime.date.today()), font=fnt, fill=kolor_font)


new_im.save("nowe.jpg")
new_im.show()

