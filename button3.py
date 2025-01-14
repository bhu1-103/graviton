from gpiozero import Button
import subprocess

button = Button(2)
button.wait_for_press()
command_to_run = "python /home/bhu4/payloads/2048-random.py"

subprocess.run(command_to_run, shell=True)

