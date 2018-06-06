# Why I've done it?   ![alt text](https://ezgif.com/images/loadcat.gif)
I've decided start learning Python syntax and here is my first project!! I'm pretty lazy so I learn by myself without taking hours of courses, they are exhausting. You will only learn practicing and setting goals so, for that reason, I want to share my practices with you so that more people have the opportunity to learn. **Ah, and... one more thing!! I am not responsible for the wrong use of this script, it has been created to help newbies!**

## Source Code
Source Code has been written using Python 3.6.5 so I recommend you to use this version, you can download it from https://www.python.org

**To build an .exe use 'pyinstaller', there are alternatives like cx_Freeze but these do not give you the option to create a single file executable.**
``` bash
#Open the windows CMD at script folder and write:

$ pyinstaller.exe --onefile --noconsole keylogger.py

#In case you do not have installed 'pyinstaller' use this cmd:

$ pip install pyinstaller
```
## Why JSON? I can't read this well!

This project does not end here, I did it to **combine with my next tool** in Python which will be a graphical interface that allows you to search by date and time the fragment what you want to read. **With this tool all special characters like accents will be readable.**

## Features
- CPU consumption is practically non-existent.
- Spanish special characters like accents are supported.
- It can be started when windows startups.
- The save is done in json format which allows having a better organization of the logs by dates.
- When the connection is lost, the script tries to reconnect with the database without losing the unsaved data.
- It is difficult to detect if you make an ingenious executable.
- Console can be hide by changing the file format to .pyw or creating an windows executable .exe
