import argparse
import json
import requests
import time
from datetime import datetime as dt
from pytz import timezone
from RPLCD.i2c import CharLCD


class DisplayStats:
	def __init__(self):
		self.api_url = 'http://pi.hole/admin/api.php'
		self.lcd = CharLCD('PCF8574', 0x27, rows=2) 
		self.tz = timezone('US/Eastern')

	def main(self):
		data = self.retrieve_data()
		data = self.parse_data(data)
		for d in data:
			self.print_to_screen(d)
			time.sleep(2)

	def retrieve_data(self):
		return json.loads(requests.get(self.api_url).text)

	def parse_data(self, data):
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
		self.lcd.clear()
		self.lcd.write_string(value)

if __name__ == '__main__':
	d = DisplayStats()
	while True:
		d.main()
