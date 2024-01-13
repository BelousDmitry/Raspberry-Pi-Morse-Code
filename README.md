# Transfering Morse Code between two Raspberry Pi computers.
Morse code is sent from one computer to another by the laser. The second computer has a sensor that detects if the laser is on/off. 
To be more exact, it turns on the laser for a time according to dot, dash, etc. The receiver reads the laser using a light sensor. 
It takes time when it detects the light(laser) and does it again when there is no light. Therefore, the program subtracts the second value of time and the first one and gets the total time the laser was on. 
Thus, it can determine whether it was a dot, dash, etc. 

## Sender
![sender](https://github.com/BelousDmitry/Raspberry-Pi-Morse-Code/assets/58919860/e7f26b5c-561d-4f40-b145-f0065f31aa9b)

## Receiver
![receiver](https://github.com/BelousDmitry/Raspberry-Pi-Morse-Code/assets/58919860/044a6718-fadd-4e1f-9b11-6fb641293a80)
