#requirements pyserial, you can do pip3 install pyserial
import serial
import sys
import time


DEVICE = '/dev/ttyACM0' # or /dev/ttyUSB0 or in windows COM1 or similar
RATE = 115200           # valid values 200,2400,4800,9600,14400,19200,38400,57600,115200,230400,460800
TIMEOUT = 1             # you can put a float in format p.e. 0.5
PRE = "AT"
phone = ""
command = ""

def hexa(s):
    '''auxiliary visualize all char for detect char non-visible'''
    st = []
    for i in s:
      st.append(ord(i))
    return st
  
def is_correct(command):
    phone.write(str.encode(PRE + command + '\r',"utf-8"))
    response = bytes.decode(phone.readall())
    if "OK" in response:
        return True
    else: 
        return False

def get_storage_info():
    '''return a clean a string with storage,number contacts, total space'''
    command = "+CPBS"
    POST = "?"
    phone.write(str.encode(PRE + command + POST + '\r',"utf-8"))
    response = bytes.decode(phone.readall())
    s = ""
    if "OK" in response:
        lines = response.replace('\r',"").split('\n')
        for l in lines:
            if command + ": " in l:
                #print (hexa(i))
                s =  l[l.index(':') + 2:].strip()
    else: 
        s += "  > ERROR 99: Command error in instruccion " + PRE + command
    return s    
    
    
    
def get_info(command):
    phone.write(str.encode(PRE + command + '\r',"utf-8"))
    response = bytes.decode(phone.readall())
    s = ""
    if "OK" in response:
        lines = response.replace('\r',"").split('\n')
        for l in lines:
            if ("OK" not in l) and (l != "") and (command not in l):
                #print (hexa(i))
                s += '\n' + l
    else: 
        s += "  > ERROR 99: Command error in instruccion " + PRE + command
    return s.strip()

def get_locations():
    '''get locations cleans'''
    command = "+CPBS"
    POST = "=?"
    phone.write(str.encode(PRE + command + POST + '\r',"utf-8"))
    response = bytes.decode(phone.readall())
    s = ""
    if "OK" in response:
        lines = response.replace('\r',"").split('\n')
        for l in lines:
            if command + ": " in l:
                #print (hexa(i))
                s =  l[l.index('(') + 1:l.index(')')]
    else: 
        s += "   > ERROR 99: Command error in instruccion " + PRE + command
    return s 

def export2vcf(lista,storage):
    '''export list to a vcf 2.1 file format'''
    out = storage.replace("\"","") + time.strftime("%Y%m%d_%H%M%S" + ".vcf")               
    s = ''
    for i in lista.split("\n"):
        if "+CPBR:" in i:
            r = i.replace("\"","").split(",")
            print(r)
            s = s + "BEGIN:VCARD\nVERSION:2.1\n"
            s = s + "N:" + r[3] + "\n"
            s = s + "FN:" + r[3] + "\n"
            s = s + "TEL;type=CELL:" + r[1] + "\n"
            s = s + "END:VCARD\n";
    try:
        f = open(out,"w")
        f.write(s)
    finally:
        f.close()
    return out
    
#inicializate
try:    
    phone = serial.Serial(DEVICE,RATE, bytesize=8, parity='N', stopbits=1, timeout=TIMEOUT, xonxoff=0, rtscts=1)
except serial.SerialException as e:
    if e.errno == 13:
        print("  > ERROR 13: Permission denied, try before: sudo chmod 666 " + DEVICE)
    elif e.errno == 2:
        print("  > ERROR 2: Could not open port, please connect the device or active modem")
    else:
        print (e)
        
#getting info: provider + model + imei
print("  > Getting info device...")
print("Provider: " + get_info("+CGMI"))
print("Model: " + get_info("+CGMM"))
print("Imei: " + get_info("+CGSN"))

#get storage locations
print("  > Checking available storages...")
#print("locations: " + get_info("+CPBR=1,99"))
locations = get_locations().split(",")
for l in locations:
    if is_correct("+CPBS=" + l): # select an storage
        info = get_storage_info()
        s = "" # [storage,contacts number,size storage]
        if "." in info:
            s = info.split(".")
        else:
            s = info.split(",")      
        print("  > Getting " + s[1] + "/" + s[2] + " records from storage " + s[0] + "...")
        records = get_info("+CPBR=1," + s[2])
        #print(records)
        print("  > Save records in " + export2vcf(records, s[0]))

print("  > Bye")
        

        
        
        
        
        