from gpiozero import LED, Button
from time import sleep

led = LED(17)
button = Button(2)

button.wait_for_press()
print("glow")
led.on()
sleep(3)
led.off()
