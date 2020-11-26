import time
import RPi.GPIO as GPIO

# de GPIO pinnen van de knop en het lampje
btnPlayPin = 27
ledPin = 4

#variabelen voor debouncing
btnTime = time.time()
debounceTime = 0.3

# houd bij of het lampje aan of uit is
ledAan = False

# deze callback functie wordt uitgevoerd wanneer de knop wordt ingedruk
def btnPlayCallback(channel):
    global btnTime, ledAan
    # reageer alleen als de knop de afgelopen 0.3 s niet is gebruikt
    if time.time() - btnTime > debounceTime:
        btnTime = time.time()
        ledAan = not ledAan
        if ledAan:
            print("Lampje aan")
        else:
            print("Lampje uit")
        GPIO.output(ledPin, ledAan)

# initialiseer de GPIO pinnen
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(btnPlayPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# koppel een verandering aan de GPIO pin aan de callback functie
GPIO.add_event_detect(btnPlayPin, GPIO.FALLING, callback = btnPlayCallback)

# maak het lampje uit
GPIO.output(ledPin, False)
print("Druk op de knop")

try:
    # doe niets (tenzij de knop wordt gebruikt)
    while True:
        continue
except KeyboardInterrupt: # wanneer het script wordt gestopt met Ctrl-C
    GPIO.cleanup() # geef de gebruikte pinnen weer vrij
