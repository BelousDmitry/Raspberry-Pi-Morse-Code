import time
import urllib.request
import RPi.GPIO as GPIO
from num2words import num2words
from subprocess import call


dot_time = 0.01
cmd_beg= 'espeak '
cmd_out= '--stdout > /home/pi/Desktop/Text.wav '

cmd_run = 'aplay /home/pi/Desktop/*'


ON = 0
OFF = 1

speakerStatus = "false"
repeat = 0



SensorPin = 26

GPIO.setmode(GPIO.BCM)       
GPIO.setup(SensorPin, GPIO.IN)





def convertIntoSentence(morse_code_string):
    file = open("morse-code.txt")
    data = file.read()
    sentence = ""
    for letter in morse_code_string.split(" "):
        for line in data.split("\n"):
            if letter == line[4:]:
                sentence = sentence + line[0]
                break
            elif letter == "/":
                sentence = sentence + " "
                break
    file.close()
    return sentence


def receiveSignals(dot_time):
    time1 = 0
    time2 = 0
    timelist = []
    give_up_time = time.time() + (dot_time * 6)
    waiting = True
    morse_code = ""
    while waiting:
        if ON == GPIO.input(SensorPin) and time1 == 0:
            time1 = time.time()
            give_up_time = time1 + (dot_time * 6)

        elif OFF == GPIO.input(SensorPin) and time1 == 0 and time.time() > give_up_time:
            waiting = False
                     
        elif OFF == GPIO.input(SensorPin) and time1 != 0:
            time2 = time.time()
            timelist.append(time2 - time1)
            time1 = 0
    
    for i in timelist:
        if i <= (dot_time + (dot_time/2)):
            morse_code = morse_code + "."
        elif i <= ((dot_time * 2) + (dot_time/2)):
            morse_code = morse_code + "-"
        elif i <= ((dot_time * 3) + (dot_time/2)):
            morse_code = morse_code + " "
        elif i <= ((dot_time * 4) + (dot_time/2)):
            morse_code = morse_code + "/"

    return morse_code
            

def saySentence(sentence):
    sentence = sentence.replace(' ', '_')
    call([cmd_beg+cmd_out+sentence], shell=True)
    call([cmd_run], shell=True)
    
def getCommand(sentence, command):
    command_id = sentence.find(command)
    sentence = sentence[command_id + len(command) + 3:]
    space_id = sentence.find(" ")
    return sentence[0:space_id]

def getText(sentence):
    text_id = sentence.find("$TEXT")
    sentence = sentence[text_id + len("$TEXT") + 3:]
    return sentence


while True:
    morse_code = receiveSignals(dot_time)
    if morse_code != "":        
        sentence = convertIntoSentence(morse_code)
        speakerStatus = getCommand(sentence, "$SPEAKER")
        repeat = getCommand(sentence, "$REPEAT")
        sentence = getText(sentence)
        repeat = int(repeat)

        while repeat > 0:
            print(sentence)
            if speakerStatus == "TRUE":
                saySentence(sentence)
            repeat = repeat - 1








