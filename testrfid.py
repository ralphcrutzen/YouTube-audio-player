# Original file: https://github.com/gassajor000/pn532pi/blob/master/examples/readMifare.py
# Edited by Ralph Crützen

import time
import binascii

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi
from pn532pi import Pn532Hsu

PN532_I2C = Pn532I2c(1)
nfc = Pn532(PN532_I2C)
nfc.begin()
nfc.SAMConfig()
vorigeUID = 0

print("Wacht op tag...")
while True:
    success = False
    #  Wait for an ISO14443A type cards (Mifare, etc.).
    while not success:
        success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

    #  Display some basic information about the card
    if uid != vorigeUID:
        vorigeUID = uid
        print("Tag gevonden!")
        print("UID: {}".format(int(binascii.hexlify(uid),16)))
        print("Wacht op tag...")
