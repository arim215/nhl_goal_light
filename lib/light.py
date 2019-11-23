import random
import platform
import pygame

if "armv" in platform.machine() :
    # import GPIO if running on RPI
    import RPi.GPIO as GPIO
else :
    # import gpio_mock if not running on RPI
    from lib import gpio_mock as GPIO


def setup():
    """ Function to setup raspberry pi GPIO mode and warnings. PIN 7 OUT and PIN 11 IN """

    # Setup GPIO on raspberry pi
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW) # Tell the program you want to use pin number 7 as output. Relay is ACTIVE LOW, so OFF is HIGH
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set GPIO 11 as a PULL DOWN switch
    GPIO.add_event_detect(11, GPIO.RISING, activate_goal_light, 5000)


def activate_goal_light(gpio_event_var=0):
    """ Function to activate GPIO for goal light and plar random audio clip. """
    songrandom = random.randint(3, 3) #Set random numbers depending on number of audio clips available
    # Prepare commande to play sound (change file name if needed)
    pygame.mixer.init()
    pygame.mixer.music.load('/home/pi/nhl_goal_light/audio/goal_horn_{SongId}.mp3'.format(SongId=str(songrandom)))
    GPIO.output(7, GPIO.HIGH) #Turn on light, active low relay, so on is low
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    GPIO.output(7, GPIO.LOW) #Turn off light


def cleanup():
    """ Function to cleanup raspberry pi GPIO at end of code """

    # Restore GPIO to default state
    GPIO.remove_event_detect(15) #Add to end of function
    GPIO.cleanup()
    print("GPIO cleaned!")
