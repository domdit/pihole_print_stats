import argparse
import json
import requests
import time
from datetime import datetime as dt
from pytz import timezone
from RPLCD.i2c import CharLCD


class DisplayStats:
	"""Queries local PiHole API and displays it on LCD
		
	Attributes:
		api_url (str):path to the pihole api, this is the generic path 
			and should work on all instances.
		lcd (CharLCD): This sets the LCD type. PCF8574 is the backback 
			that came with my LCD. You may need to update this value
			with the value of the backpack of your LCD
		tz (timezone): Update this to your timezone
		sleep_time (int): time in seconds between display changes.
			Update this value to your preference.
	"""
	
	def __init__(self):
		self.api_url = 'http://pi.hole/admin/api.php'
		self.lcd = CharLCD('PCF8574', 0x27, rows=2)
		self.tz = timezone('US/Eastern')
		self.sleep_time = 2

	def main(self):
		"""Platform for sequentially calling class methods"""
		
		data = self.retrieve_data()
		data = self.parse_data(data)
		for d in data:
			self.print_to_screen(d)
			time.sleep(self.sleep_time)

	def retrieve_data(self):
		"""Queries PiHole API and returns response as a JSON object"""
		return json.loads(requests.get(self.api_url).text)

	def parse_data(self, data):
		"""Parses darta returned from API into human readable format
		
		Arguments:
			data (json): API json object
		Notes:
			The values here are customizable. I recommend you look
			at the API output to see if there are any other data
			points that may be of interest.
		"""
		
		parsed_data = [
			'Domains Blocked:\n\r{}'.format(data['domains_being_blocked']),
			'Queries Today:\n\r{}'.format(data['dns_queries_today']),
			'Blocked Today:\n\r{}'.format(data['ads_blocked_today']),
			'Ad Percentage:\n\r{}'.format(data['ads_percentage_today']),
			'Unique Domains:\n\r{}'.format(data['unique_domains']),
			'pi.hole/admin\n\rfor more info',
			dt.now(self.tz).strftime('%m/%d/%Y\n\r%I:%M %p')
		]

		return parsed_data

	def print_to_screen(self, value):
		"""Writes data to screen
		Arguments:
			value (str): value to print to screen
		"""
		
		self.lcd.clear()
		self.lcd.write_string(value)

if __name__ == '__main__':
	d = DisplayStats()
	while True:
		d.main()
