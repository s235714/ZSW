import sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 7

while True:
    
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print(str(temperature) + ' °C and ' + str(humidity) + '%')
