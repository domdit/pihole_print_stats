import argparse
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27, rows=2)

def print_to_screen(value):
	lcd.clear()
	lcd.write_string(value)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('value', type=str)
	args = parser.parse_args()
	print_to_screen(args.value)
