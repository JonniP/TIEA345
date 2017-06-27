import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

carRed = 16
carYellow = 20
carGreen = 21

pedClicked = 6
pedRed = 19
pedGreen = 26

button = 13
sensor = 12

GPIO.setup(button, GPIO.IN)
GPIO.setup(sensor, GPIO.IN)

GPIO.setup(carRed, GPIO.OUT)
GPIO.setup(carYellow, GPIO.OUT)
GPIO.setup(carGreen, GPIO.OUT)

GPIO.setup(pedRed, GPIO.OUT)
GPIO.setup(pedGreen, GPIO.OUT)
GPIO.setup(pedClicked, GPIO.OUT)

def initialize():
	print("initializing...")
	GPIO.output(carGreen, 1)
	GPIO.output(carYellow, 0)
	GPIO.output(carRed, 0)
	
	GPIO.output(pedGreen, 0)
	GPIO.output(pedRed, 1)
	GPIO.output(pedClicked, 0)

def setCarGreen():
	print("car green")
	GPIO.output(pedRed, 1)
	GPIO.output(pedGreen, 0)

	time.sleep(2)
	GPIO.output(carYellow, 1)
	GPIO.output(carRed, 0)
	GPIO.output(carGreen, 0)
	time.sleep(2)

	GPIO.output(carGreen, 1)
	GPIO.output(carYellow, 0)

def setPedGreen():
	print("ped green")
	GPIO.output(carGreen, 0)
	GPIO.output(carRed, 0)
	GPIO.output(carYellow, 1)
	time.sleep(2)

	GPIO.output(carYellow, 0)
	GPIO.output(carRed, 1)
	time.sleep(2)

	GPIO.output(pedRed, 0)
	GPIO.output(pedClicked, 0)
	GPIO.output(pedGreen, 1)

	time.sleep(5)
	setCarGreen()

def start():
	time.sleep(2)
        setPedGreen()
	time.sleep(2)


initialize()

end = time.time() + 15
clicked = False
maxWaitTime = 0
while time.time() < end:
	buttonState = GPIO.input(button)

	if buttonState is GPIO.HIGH:
		maxWaitTime = time.time() + 5 
		clicked = True
		GPIO.output(pedClicked, 1)
			
	else:
		if clicked:
                	motion = GPIO.input(sensor)
                	if motion is 0:
                        	clicked = False
				start()
                	if motion is 1 and time.time() >= maxWaitTime:
				clicked = False
				start()
			if motion is 1 and time.time() < maxWaitTime:
				print("Heavy traffic")                      
		else:
			print("NO CLICK DETECTED")

	time.sleep(1)

GPIO.cleanup()