# lcd-web

A daemon that writes incoming messages from a web socket to a LCD with i2c using my lcd-i2c module.
For this program to work, the LCD_i2c.py file from my lcd-i2c repo has to be in the same directory
as the lcd-web.py program.

# Options

lcd-web accepts the following arguments:

```
-h, --help          display help message
-p, --port          specify which port lcd-web should listen at
-b, --buffer-size   specify the buffer size
-v, --verbose       change verbosity
```
All arguments are optional.
