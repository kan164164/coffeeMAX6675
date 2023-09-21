#!/usr/bin/env python3
import spidev

dummyData = [0x00,0x00]

spi = spidev.SpiDev()
spi.open(0, 0)          # bus 0,cs 0

# Settings
spi.max_speed_hz = 1000000      # 1MHz
spi.mode = 3                    # SPI mode : 3

readByteArray = spi.xfer2(dummyData)
temperatureData = ((readByteArray[0] & 0b01111111) << 5) | ((readByteArray[1] & 0b11111000) >> 3)
temperature = temperatureData * 0.25
print(str(temperature))

spi.close
