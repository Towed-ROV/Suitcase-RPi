# Suitcase-RPi
Author of surface unit softare: Sophus
suitcase controll for the RPi
this software controlls the NMEA sensors in the siutcase, parses the data and sends it over ethernet.

The system can add more sensors, but the limiting factor is the amount of ports on the RPi
the system also meshures the distance and sends a boolean value to confirm that it has traveld a set distance.



python v3.6 +
remember to run 
py -m pip install -r requirements.txt


Running at boot:
when Runing a program on startup with an RPi  there are several possible solutions, 
one solution is to open the .bashrc file using the command "sudonano /home/pi/.bashrc" 
and then add "echo Running at boot" and  "sudo python /home/pi/sample.py" at the end of the file. 
when the RPi is rebooted or when a terminal is started the program will start to run. 



SETTING UP A RPi with multiple serial coms
The RPi 4 supports six $RX \backslash TX$ and the earlier RPi's support two connections by converting GPIO pins to UART. 
But only one UART is enabled initially. To use the additional pins, some settings have to be changed in the RPi.

First, to enable the primary UART open the "raspi-config" select interface options - serial port. 
Then set "login shell to be accessible over serial" to NO and "serial port hardware to be enabled" to YES. 
Exit the settings, open "confix.txt" add enable$\_$uart$=1$ save and close, then reboot the RPi.


There is also a serial port currently used by the Bluetooth of the RPi, to use this open "config.txt" and add "dtoverlay=disable-bt" to the end of the text file.
To add multiple ports on the RPi 4, open the "config.txt" file and add "dtoverlay=uart$\#$" where $\#$ is the UART you want to enable. 
The four additional UARTS are numbered as 1, 2, 3 and 4. 

The UART's can be accessed in the RPi with the address "/dev/ttyAMA$\#$" where $\#$ is a number between 0 and 4 for the serial ports. 
To get the pins that are used by the UART's use the "raspi-gpio funcs" command in the console.


these sites for more info about setting up uart
https://www.raspberrypi.org/documentation/configuration/uart.md
https://www.raspberrypi.org/forums/viewtopic.php?t=244827
