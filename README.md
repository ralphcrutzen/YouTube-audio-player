# Youtube playlist audio player

This repository provides the Python 3 code for a music player which plays YouTube playlists. You can select different playlists with NFC tags. Status and song information are displayed on a 16x2 lcd screen. Play/pause, next/previous track and volume up/down are controlled with 5 buttons.


I built this into a small wooden treasure chest.

Hardware used:
* Raspberry Pi Zero W
* Adafruit speaker bonnet
* 4 Ohm 3 Watt speakers
* 5 buttons (including one big arcade button with led light)
* 16x2 I2C LCD screen
* I2C PN532 RFID scanner

![circuit](https://github.com/ralphcrutzen/YouTube-audio-player/blob/main/images/circuit.png)

Software installation:
* Raspberry Pi OS Lite
* I2S support for the Adafruit speaker bonnet
  * `curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash`
* pip for Python 3
  * `sudo apt install python3-pip`
* pafy library for Python 3
  * `sudo pip3 install pafy`
* vlc and the vlc library for Python 3
  * `sudo pip3 install python-vlc`
  * `sudo apt install vlc`
* youtube-dl library for Python 3
  * `sudo pip3 install youtube_dl`
* lcd library for Python 3
  * `git clone https://github.com/the-raspberry-pi-guy/lcd.git`
  * `cd lcd`
  * `sudo sh install.sh`
  * `cd`
  * `cp lcd/lcddriver.py lcd/i2c_lib.py ~`
* I2C tools
  * `sudo apt install python3-smbus`
  * `sudo apt install i2c-tools`
* GPIO library for Python 3
  * `sudo apt install python3-rpi.gpio`
* PN532 rfid library for Python 3
  * sudo pip3 install pn532pi

Use the `test*.py` scripts to test the different hardware parts.
`ytplayer.py` is the main script which brings all together. Put `python3 /home/pi/ytplayer.py &` in `/etc/rc.local` (before the lin `exit 0` to execute this script at startup.

The 'welcome' sound file was downloaded from [freesound.org](https://freesound.org/people/Timbre/sounds/98522/)
