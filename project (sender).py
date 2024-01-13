import time
import urllib.request
import RPi.GPIO as GPIO


dot_time = 0.01
delay = dot_time
prev_text = ""



using_wire = False
if using_wire:
    laser_on = GPIO.LOW
    laser_off = GPIO.HIGH
else:
    laser_on = GPIO.HIGH
    laser_off = GPIO.LOW

LaserPin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(LaserPin, GPIO.OUT)




def webRead(URL):
    try:
        print("Trying to open "+URL)
        h = urllib.request.urlopen(URL)
        print("Opened "+URL)
        response = h.read()
        print(len(response)," chars in the response")
    except:
        print("Houston? We have a problem. Can't open "+URL)
        response = "error"
    return response



def convertIntoMorseCode(message):
    file = open("morse-code.txt")
    data = file.read()
    morse_code_string = ""
    for letter in message:
        letter = letter.upper()
        for line in data.split("\n"):
            if line[0] == letter:
                morse_code_string = morse_code_string + line[3:]
                break
            elif letter == " ":
                morse_code_string = morse_code_string +  " /"
                break
    
    file.close()
    return morse_code_string.lstrip()




def sendSignals(morse_code_string, dot_time):
    for i in morse_code_string:
        if i == ".":
            GPIO.output(LaserPin, laser_on)
            time.sleep(dot_time)
            GPIO.output(LaserPin, laser_off)
            time.sleep(delay)
        if i == "-":
            GPIO.output(LaserPin, laser_on)
            time.sleep(dot_time * 2)
            GPIO.output(LaserPin, laser_off)
            time.sleep(delay)
        if i == " ":
            GPIO.output(LaserPin, laser_on)
            time.sleep(dot_time * 3)
            GPIO.output(LaserPin, laser_off)
            time.sleep(delay)
        if i == "/":
            GPIO.output(LaserPin, laser_on)
            time.sleep(dot_time * 4)
            GPIO.output(LaserPin, laser_off)
            time.sleep(delay)

def getValue(data, searchfor):
    starting_point = data.find(searchfor.encode())
    starting_point = starting_point + len(searchfor)
    searchfor = "<span>"
    starting_point = data.find(searchfor.encode(), starting_point)
    searchfor = "</span>"
    ending_point = data.find(searchfor.encode(), starting_point)
    value = data[starting_point+6:ending_point]
    value = value.decode("utf-8")
    return value


while True:
    # Initially, it took all the information from the website. 
    # It was a convenient user interface instead of hard-coded values. 
    # But the website is no longer there. 
    
    # data = webRead("https://morse-code-unh.herokuapp.com")
    # speakerStatus = getValue(data, "Activate speaker:")
    # repeat = getValue(data, "Repeat:")
    # text = getValue(data, "Text:")
    speakerStatus = "TRUE"
    repeat = 1
    text = "Hello World"

    if text != prev_text:
        sentence = "$speaker = " + speakerStatus + " $repeat = " + repeat + " $text = " + text
        morse_code = convertIntoMorseCode(sentence)
        sendSignals(morse_code, dot_time)
        prev_text = text
    
    time.sleep(3)







