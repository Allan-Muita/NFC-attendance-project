#
# RFID Read
#

import sys
import time
import json
import rfidiot
from nyamuk import nyamuk
import nyamuk.nyamuk_const as NC
from nyamuk import event

# Functions
def open_reader():
	""" Attempts to open the card reader """
	try:
		card = rfidiot.card
		return card
	except:
		print "Couldn't open reader!"
		sys.exit()
		return None

def listen(card, interval):
	""" Listens for a card to be placed on the reader """
	
	while 1:	
		if card.select():
			data = json.dumps({"card_info":
				[{"card_id": card.uid}, {"timedate": get_time()}, {"action": "Placed"}]})
			ny.publish(ny_topic, data)
			ny.loop()
			break
		print 'Waiting: Card Placement'
		time.sleep(interval)
	return card.uid

def listen_remove(card, interval, card_id):
	""" Listens for a card to be placed on the reader """
	while 1:
		if not card.select():
			data = json.dumps({"card_info":
				[{"card_id": card_id}, {"timedate": get_time()}, {"action": "Removed"}]})
			ny.publish(ny_topic, data)
			ny.loop()
			break
		print "Waiting: Card Removal"
		time.sleep(interval)

def get_time():
	""" Returns a string with the time and date """
	return time.strftime("%a, %d %b %Y %H:%M:%S + 0000", time.gmtime())

ny_server = "test.mosquitto.org"
ny_client = "RFID-Reader"
ny_topic = "/nyamuk/test"

# Open the card reader
card = open_reader()
card_info = card.info('cardselect v0.1m')

# Connect to the MQTT Server
ny = nyamuk.Nyamuk(ny_client, server = ny_server)
print "Connecting..."
rc = ny.connect()

# Check for a successfull connection
if rc != NC.ERR_SUCCESS:
    print "Can't connect"
    sys.exit(-1)
print "Connected!"

# Main loop
while 1:
	card_id = listen(card, 0.1)
	listen_remove(card, 0.1, card_id)
