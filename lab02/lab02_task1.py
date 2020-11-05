import Adafruit_CharLCD as LCD
import os
import datetime
import commands

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
                       
def getTimeText():
    t=datetime.datetime.now()
    hours= str(t.hour)
    minutes =str(t.minute)
    seconds=str(t.second)
    timetext= hours + ':' + minutes + ':' + seconds
    return timetext

def getIP():
    return "ip:" + commands.getoutput('hostname -I')

def getTimeTemp():
    return getTimeText() + "\n"  + getCPUtemperature()


lcd=LCD.Adafruit_CharLCDPlate()

lcd.set_color(1, 0, 0)

cpu_temp=getCPUtemperature()

cpu_time=getTimeText()
cpu_ip=getIP()
cpu_timetemp=getTimeTemp()



lcd.message('Press Left \nor Right Button')



print('Press Ctrl-C to quit.')
while True:
    buttons = ( (LCD.SELECT, '', (1,0,0)),
            (LCD.LEFT,   getCPUtemperature()  , (1,0,0)),
            (LCD.UP,     getIP()  , (1,0,0)),
            (LCD.SELECT,   getTimeTemp()  , (1,0,0)),
            (LCD.RIGHT,  getTimeText() , (1,0,0)) )
    for button in buttons:
        if lcd.is_pressed(button[0]):
 
            lcd.clear()
            lcd.message(button[1])
            lcd.set_color(button[2][0], button[2][1], button[2][2])
