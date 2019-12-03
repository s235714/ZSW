from urllib.request import urlopen

import numpy
from bs4 import BeautifulSoup
import re
import urllib.request
import os.path
import random
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import PIL
import datetime

import tweepy
import Adafruit_DHT
import sounddevice as sd
from scipy.io.wavfile import write
from time import gmtime, strftime
from scipy.io import wavfile as wav
import os
import time

# Authenticate to Twitter
auth = tweepy.OAuthHandler("Y509knpZaOHKERLudDQ5yCa1a",
                           "WOpjxR4FFAuEXgTvZ5gSqPBWAkgem8r82XyKnyV4kfAjOPxvh0")
auth.set_access_token("1182367262453518336-C50nxYQTZwKZrmLuHleyorIvSVUO95",
                      "wvRMz5fqiHGhS6JOQqXDt5l40cw5yrA1IBfJNZV3vQHYg")


def get_sound():
    timestamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

    ts = str(timestamp) + ".wav"
    print(ts)

    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(ts, fs, myrecording)  # Save as WAV file

    rate, data = wav.read(ts)
    data1 = numpy.absolute(data)  # uzyskiwanie samych dodatnych wartosci
    data1 = numpy.sort(data1, axis=0)  # posortowanie wartosci

    wartoscGlosnosci = len(data1) / 100 * 95  # bierzemy 95 percentyl

    poziomHalasu = round(20 * numpy.log10(data1[wartoscGlosnosci][0]), 2) + 100

    min = 100
    max = 0
    sum = 0

    with open("dane.txt", 'r') as f:
        x = f.readlines()

    for value in x:
        a = float(value)
        sum += a
        if a < min:
            min = a
        if a > max:
            max = a

    average = sum / len(x)
    average = round(average, 2)

    print("minimum: " + str(min))
    print("maximum: " + str(max))

    # dzielimy przedzial na 5 czesci i zaleznie od tego w ktorej czesci znajduje sie probka bedzie okreslane czy glosno, cicho itp
    poczatek = 0
    if (min + max) / 2 >= average:
        print("srodek powyzej sredniej")
        szerokoscPoziomu = (average - min) / (2.5)
        print(szerokoscPoziomu)
        poczatek = min
    else:
        print("srodek ponizej sredniej")
        szerokoscPoziomu = (max - average) / (2.5)
        print(szerokoscPoziomu)
        poczatek = max - 5 * szerokoscPoziomu

    if poczatek + szerokoscPoziomu > poziomHalasu >= 0:
        halasString = "bardzo cicho"
    if poczatek + 2 * szerokoscPoziomu > poziomHalasu >= poczatek + szerokoscPoziomu:
        halasString = "cicho"
    if poczatek + 3 * szerokoscPoziomu >= poziomHalasu >= poczatek + 2 * szerokoscPoziomu:
        halasString = "przecietnie glosno"
    if poczatek + 4 * szerokoscPoziomu >= poziomHalasu > poczatek + 3 * szerokoscPoziomu:
        halasString = "glosno"
    if 150 >= poziomHalasu > poczatek + 4 * szerokoscPoziomu:
        halasString = "bardzo glosno"

    os.remove(ts)
    return min, max, timestamp, poziomHalasu, halasString


def to_file(min, max, timestamp, sensors):
    list = os.listdir(r".")

    nazwa = "dane.txt"

    # jakiestam przetwarzanie ocena tego czy jest glosno czy cicho, najlepiej w dB
    # moze cos takiego https://github.com/SuperShinyEyes/spl-meter-with-RPi

    if nazwa in list:
        f = open("dane.txt", "a")
        f.write(str(timestamp) + " " + str(min) + " " + str(max) + " " + str(sensors["temperature"]) \
                + " " + str(sensors["humidity"]) + " " + (sensors["loudnessStr"]) + "\n")
        f.close()
    else:
        f = open("dane.txt", "x")
        f.write(str(timestamp) + " " + str(min) + " " + str(max) + " " + str(sensors["temperature"]) \
                + " " + str(sensors["humidity"]) + " " + (sensors["loudnessStr"]) + "\n")
        f.close()


def auth_twitter():
    api = tweepy.API(auth)

    # Verify all's ok
    try:
        api.verify_credentials()
        print("Lookin' good sire!")
        return True
    except:
        print("Yer effed up mate!")
        return False


def init_twitter():
    # Create API object
    return tweepy.API(auth, wait_on_rate_limit=True,
                      wait_on_rate_limit_notify=True)


def post_update(api, sensor_data):
    message_body = "Today's temperature: " + str(sensor_data["temperature"]) + "°C\n" \
                                                                               "Humidity: " + str(
        sensor_data["humidity"]) + "%\n" \
                                   "Loudness: " + str(sensor_data["loudness"])
    api.update_with_media("nowe.jpg", message_body)
    print("Status uploaded!")


def get_temp():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    return temperature


def get_humi():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    return humidity


def make_img(sensory):
    html = urlopen('https://www.flickr.com/search/?q=flowers')
    bs = BeautifulSoup(html, 'html.parser')

    images = re.findall("[a-z \- A-Z 0-9 \. ]+\.com[a-z \- A-Z 0-9 \. \/ \_ \-]+\.jpg", str(bs))

    licznik = 1

    for image in images:
        urllib.request.urlretrieve('https://' + str(image), 'img' + str(licznik) + '.jpg')
        print('pyk')
        licznik = licznik + 1

    print('pobrano')
    licznik -= 1
    list = os.listdir(r".")

    list.remove('obraz.py')

    wybor = random.randrange(1, 25)

    file_name = list[wybor]

    # ------------------------------

    im = Image.open(file_name)
    x, y = im.size

    mnoznik = 2
    new_x = x * mnoznik
    new_y = y * mnoznik
    im = im.resize((new_x, new_y), PIL.Image.NEAREST)

    im = im.filter(ImageFilter.GaussianBlur(4))

    pixels = im.load()

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r, g, b = pixels[i, j]
            r += 60
            g += 60
            b += 60
            if (r > 255):
                r = 255
            if (b > 255):
                b = 255
            if (g > 255):
                g = 255
            pixels[i, j] = (r, g, b)

    color = (0, 0, 255)

    fnt = ImageFont.truetype('Comic Sans MS.ttf', 40)

    d = ImageDraw.Draw(im)

    row1 = "WITAMY"
    row2 = "SERDECZNIE"

    w1, h1 = d.textsize(row1, font=fnt)
    w2, h2 = d.textsize(row2, font=fnt)

    print(str(w1))
    print(str(w2))

    print(str(new_x))

    d.text(((new_x / 2) - (w1 / 2), (new_y / 2 - h1)), row1, font=fnt, fill=color)
    d.text(((new_x / 2) - (w2 / 2), (new_y / 2 + h1)), row2, font=fnt, fill=color)

    off1 = 60
    off2 = 150

    kolor_tla = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))

    img = Image.new('RGB', (new_x, off2), color=kolor_tla)

    img1 = Image.new('RGB', (new_x, off1), color=kolor_tla)

    total_width = new_x
    max_height = new_y + off1 + off2

    new_im = Image.new('RGB', (total_width, max_height))

    images = [img1, im, img]

    x_offset = 0
    for i in images:
        new_im.paste(i, (0, x_offset))
        x_offset += i.size[1]

    temp = str(sensory["temperature"])
    wilgonosc = str(sensory["humidity"])
    halas = str(sensory["loudness"])

    kolor_font = (255 - kolor_tla[0], 255 - kolor_tla[1], 255 - kolor_tla[2])

    d1 = ImageDraw.Draw(new_im)
    d1.text((10, off1 + new_y), "temperatura: " + temp + "°C", font=fnt, fill=kolor_font)
    d1.text((10, off1 + new_y + 45), "wilgotnosc: " + wilgonosc + "%", font=fnt, fill=kolor_font)
    d1.text((10, off1 + new_y + 90), "halas: " + halas, font=fnt, fill=kolor_font)
    d1.text((10, 0), "Dzis jest: " + str(datetime.date.today()), font=fnt, fill=kolor_font)

    new_im.save("nowe.jpg")


if __name__ == "__main__":

    auth_twitter()
    api = init_twitter()

    while True:
        time.sleep(3600)
        min, max, timestamp, poziomHalsu, halasString = get_sound()
        sensor_data = {"temperature": get_temp(), "humidity": get_humi(), "loudness": poziomHalsu, "loudnessStr": halasString}
        to_file(min, max, timestamp, sensor_data)
        make_img(sensor_data)
        post_update(api, sensor_data)
