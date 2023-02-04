import spidev
import time
import datetime

dummyData = [0x00,0x00]

spi = spidev.SpiDev()
spi.open(0, 0)          # bus 0,cs 0

# Settings
spi.max_speed_hz = 1000000      # 1MHz
spi.mode = 3                    # SPI mode : 3

while 1:
        dt_now = datetime.datetime.now()
        readByteArray = spi.xfer2(dummyData)
        temperatureData = ((readByteArray[0] & 0b01111111) << 5) | ((readByteArray[1] & 0b11111000) >> 3)
        temperature = temperatureData * 0.25
        print(dt_now.strftime('%Y/%m/%d %H:%M:%S') + ',' + str(temperature))
        time.sleep(0.5)

spi.close
