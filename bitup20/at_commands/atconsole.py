#requirements pyserial, you can do pip3 install pyserial
import serial
import sys

DEVICE = '/dev/ttyACM0'
RATE = 115200 #115200 #1200,2400,4800,9600,14400,19200,38400,57600,115200,230400,460800
TIMEOUT = 1 # you can put 0.5

#inicializate
print ("Little at command console by @nomed1")

phone = serial.Serial(DEVICE,RATE, bytesize=8, parity='N', stopbits=1, timeout=TIMEOUT, xonxoff=0, rtscts=1)
command = ""

while (command != "exit"):
  command = input("$> ")
  if (command != "exit"):
    phone.write(str.encode(command + '\r',"utf-8"))
    response = bytes.decode(phone.readall(),errors="ignore")
    print (response)


print ("Disconnecting ...")
phone.close()
