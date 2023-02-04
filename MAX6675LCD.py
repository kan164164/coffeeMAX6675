#!/usr/bin/env python3
import LCD1602
import smbus
import time
import datetime
import spidev

def main():
	try:
		dummyData = [0x00,0x00]
		spi = spidev.SpiDev()
		spi.open(0, 0)          # bus 0,cs 0

		# Settings
		spi.max_speed_hz = 1000000      # 1MHz
		spi.mode = 3                    # SPI mode : 3
	except:
		LCD1602.write(0, 0, 'ERROR           ')
		LCD1602.write(0, 1, '                ')	
		exit()
	start_now = datetime.datetime.now()
	start_time = time.time()
	while True:
		try:
			dt_now = datetime.datetime.now()
			t = dt_now
			dt_time = time.time()
			elapsed_time = dt_time - start_time
			elapsed_hour = elapsed_time // 3600
			elapsed_minute = (elapsed_time % 3600) // 60
			elapsed_second = (elapsed_time % 3600 % 60)
			
			readByteArray = spi.xfer2(dummyData)
			temperatureData = ((readByteArray[0] & 0b01111111) << 5) | ((readByteArray[1] & 0b11111000) >> 3)
			temperature = temperatureData * 0.25
			roomtemp = temperature
			
			print ("時間：%s , 経過:%.f , 温度: %-4.2f C" % (t.strftime("%Y/%m/%d %H:%M:%S") , elapsed_time , roomtemp))
			LCD1602.write(0, 0,  ("%2.f min %2.f sec" % (elapsed_minute , elapsed_second)))
			LCD1602.write(0, 1,  ("%-4.2f \xdfC" % (roomtemp)))
			f = open('./MAX6675_' + t.strftime("%Y%m%d") + '.txt', mode='a', encoding='utf-8')
			f.write(t.strftime("%Y/%m/%d %H:%M:%S") + ",%-4.2f" % (roomtemp) + "\n")
			f.close()
		except:
			try:
				LCD1602.write(0, 0, 'ERROR           ')
				LCD1602.write(0, 1, '                ')	
			except:
				pass
		time.sleep(1)

def setup():
	LCD1602.init(0x27, 1) # init(slave address, background light)
	LCD1602.write(0, 0, '')
	LCD1602.write(0, 1, '')


def destroy2():
	LCD1602.init(0x27, 0) # init(slave address, background light)
	LCD1602.write(0, 0, '')
	LCD1602.write(0, 1, '')	

if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy2()

