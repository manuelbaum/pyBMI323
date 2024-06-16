This is a minimal python driver for the Bosch BMI323 chip. I'm running this on a raspberry pi zero 2w with
my own hat pcb, but if you know what you're doing you can probably adapt this easily. I wrote this code against the
[official documentation](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi323-ds000.pdf)

Important notes:

I'm using the legacy i2c interface and the i2c address of my chip is 0x68 because the SDA pin on my hat is pulled to
GND. You might want to check your chip's i2c address using something like the i2cdetect executable.