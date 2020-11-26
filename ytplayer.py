#!/usr/bin/python3
# -*- coding: utf-8 -*-

###############################################################################
# Scroll naar regel 80
# voor het invoeren van tag ID's en YT playlist url's
###############################################################################

# hulplibraries
import time, binascii, threading

# rfid libraries
from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi
from pn532pi import Pn532Hsu
import binascii

# lcd scherm library
import lcddriver

# geluid/muziek libraries
import vlc, pafy

# gpio libraries voor knoppen
import RPi.GPIO as GPIO

# initialiseer rfid
PN532_I2C = Pn532I2c(1)
nfc = Pn532(PN532_I2C)
nfc.begin()
nfc.SAMConfig()
prevUID = None

# initialiseer lcd scherm
display = lcddriver.lcd()
dispTime = time.time()  # Timer for clearing line 2 after a couple of seconds
dispClearFlag = False   # Flag to signal if display line 2 needs to be cleared

# initialiseer geluid
vlcInstance = vlc.Instance("--aout=alsa")   # Alsa is needed for speaker bonnet
player = vlcInstance.media_player_new()
player.audio_set_volume(50)

# initialiseer knoppen
btnNextPin = 17
btnPlayPin = 27
btnPrevPin = 22
btnVolUpPin = 23
btnVolDownPin = 24
ledPin = 4
btnTime = time.time()   # Timer for debouncing buttons
debounceTime = 1.5
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(btnPlayPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(btnNextPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(btnPrevPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(btnVolUpPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(btnVolDownPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.output(ledPin, False)

# playlist status
currentTrack = -1
paused = False
trackList = []      # List of links to audio streams
trackNameList = []  # List of tracknames
plLoaded = False    # Is playlist loaded

# gebruikers
class Card:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
cardList = []
currentUser = None  # Current user name

# Vul de lijst aan met tag id's, namen en playlist url's
# De tag id's kun je achterhalen met testrfid.py
cardList.append(
    Card(123456789, # Hier de id van tag
         "Naam", # hier de naam van de tag
         "Url" # hier de url van de YouTube playlist
    )
)
# Voorbeeld:
cardList.append(
    Card(1233135554,
         "Ralph",
         "https://www.youtube.com/playlist?list=PLLQdvrCajN7QJeclf7blmZJgM7TCzP_AI"
    )
)

# Callback functies

# Play / pause knop
def btnPlayCallback(channel):
    global btnTime, paused, player
    if time.time() - btnTime > debounceTime:
        btnTime = time.time()
        print("btnPlay")
        if player.get_state() == 5: # statuscode 5 = gepauzeerd
            print("Start playing")
            display.lcd_clear()
            paused = False
            playTrack(currentTrack)
            GPIO.output(ledPin, True)
        else:
            if paused == False:
                paused = True
                player.pause()
                GPIO.output(ledPin, False)
                disp("Pause", 2)
            else:
                paused = False
                player.pause()
                GPIO.output(ledPin, True)
                display.lcd_clear()


# Volgende track
def btnNextCallback(channel):
    global btnTime, currentTrack
    if time.time() - btnTime > debounceTime and plLoaded:
        btnTime = time.time()
        print("btnNext")
        GPIO.output(ledPin, True)
        currentTrack = currentTrack + 1
        if currentTrack >= len(trackList):
            currentTrack = 0
        playTrack(currentTrack)
        GPIO.output(ledPin, True)
        print("currentTrack: " + str(currentTrack))


# Vorige track
def btnPrevCallback(channel):
    global btnTime, currentTrack
    if time.time() - btnTime > debounceTime and plLoaded:
        btnTime = time.time()
        print("btnPrev")
        GPIO.output(ledPin, True)
        currentTrack = currentTrack - 1
        if currentTrack < 0:
            currentTrack = len(trackList) - 1
        playTrack(currentTrack)
        GPIO.output(ledPin, True)
        print("currentTrack: " + str(currentTrack))


# Volume omhoog
def btnVolUpCallback(channel):
    global vol, dispTime, dispClearFlag
    print("btnVolUp")
    #if plLoaded:
    dispTime = time.time()
    dispClearFlag = True
    vol = player.audio_get_volume() + 5
    if vol > 100:
        vol = 100
    player.audio_set_volume(vol)
    disp("Volume: " + str(vol), 2)


# Volume omlaag
def btnVolDownCallback(channel):
    global vol, dispTime, dispClearFlag
    print("btnVolDown")
    #if plLoaded:
    dispTime = time.time()
    dispClearFlag = True
    vol = player.audio_get_volume() - 5
    if vol < 0:
        vol = 0
    player.audio_set_volume(vol)
    disp("Volume: " + str(vol), 2)


def disp(txt, line):
    display.lcd_display_string((txt + "                ")[:16], line)
    print(txt)


def playTrack(track):
    global paused
    paused = False
    GPIO.output(ledPin, True)
    media = vlcInstance.media_new(trackList[track])
    player.set_media(media)
    player.play()
    disp(str(track + 1) + " " + trackNameList[track], 1)


def playWelcomeSound():
    player.stop()
    currentTrack = -1
    media = vlcInstance.media_new('/home/pi/welcome.mp3')
    player.set_media(media)
    player.play()


def loadPlaylist(pl):
    global trackList, btnTime, paused, currentTrack, trackNameList, plLoaded
    plLoaded = False
    currentTrack = 0
    playlist = pafy.get_playlist(pl)
    nItems = len(playlist['items'])
    trackList = []
    trackNameList = []
    for i in range(nItems):
        track = playlist['items'][i]['pafy']
        trackNameList.append(track.title)
        disp("Laden: " +  str(i + 1) + "/" + str(nItems), 2)
        url = track.getbestaudio().url
        trackList.append(url)
        time.sleep(0.2)
        if i == 0: # play 1st track before tracklist is fully loaded
            playTrack(0)
    disp(str(currentTrack + 1) + " " + trackNameList[currentTrack], 1)
    disp("", 2)
    btnTime = time.time()
    plLoaded = True


GPIO.add_event_detect(btnPlayPin, GPIO.FALLING, callback = btnPlayCallback)
GPIO.add_event_detect(btnNextPin, GPIO.FALLING, callback = btnNextCallback)
GPIO.add_event_detect(btnPrevPin, GPIO.FALLING, callback = btnPrevCallback)
GPIO.add_event_detect(btnVolUpPin, GPIO.FALLING, callback = btnVolUpCallback)
GPIO.add_event_detect(btnVolDownPin, GPIO.FALLING, callback = btnVolDownCallback)


def main():
    global currentUser, prevUID, currentTrack, dispClearFlag
    disp("Wacht op tag...", 1)
    while True:
        if player.get_state() == 6 and plLoaded: # end of playlist track
            currentTrack += 1
            if currentTrack >= len(trackList):
                currentTrack = 0
            playTrack(currentTrack)
        # clear display status (pause, volume) after 2 seconds
        if dispClearFlag and time.time() - dispTime > 2:
            if paused:
                disp("Pause", 2)
            else:
                display.lcd_clear()
            dispClearFlag = False
        #  Wait for an ISO14443A type cards (Mifare, etc.).
        success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
        if (success):
            cardId = int(binascii.hexlify(uid), 16)
            print("Tag gevonden: " + str(cardId))
            if uid != prevUID:
                for c in cardList:
                    if c.id == cardId:
                        player.stop()
                        playWelcomeSound()
                        prevUID = uid
                        currentUser = c.name
                        disp("Tag: " + currentUser, 1)
                        loadPlaylist(c.url)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        # Am I cleaning up thoroughly enough?
        display.lcd_clear()
        GPIO.output(ledPin, False)
        del display
        del nfc
        del PN532_I2C
        del player
        del vlcInstance
        GPIO.cleanup()
