import time
import requests
import argparse
from json import loads as json_parse
from requests.exceptions import RequestException
from color import cprint_red, cprint_blue, cprint_green

TWITCH_LINK = "https://www.twitch.tv/"
API_LINK 	= "https://api.twitch.tv/"
CLIENT_ID   = "owpia6t4yoo37fxnq372oq39jzauon"

def parse_arguments( ):
	parser = argparse.ArgumentParser(description="Twtich scraper")
	parser.add_argument("-v","--verbosity", help="Verbosity level of debugging (1-3)", type=int, required=False)
	parser.add_argument("-f", "--file", help="Path to file of streamers to scrape", type=str, required=True)

	return parser.parse_args( )

class Streamer(object):

	def __init__(self, name):
		self.name = name.rstrip( )

		#Alot of streamer's names are just their login names with capitals, i.e. IWillDominate,
		#so I juse have the capitalised version for shit like saving it into files.
		self.login = self.name.lower( )
		self.last_test = False

	def __repr__(self):
		return "<Streamer {}>".format(self.name)

	def is_online(self):
		cprint_green("[*] Checking if streamer {} is online".format(self.name))
		try:
			r = requests.get("{}/helix/streams?user_login={}".format(API_LINK, self.login), headers={
				"Client-id": CLIENT_ID
			})
		except RequestException:
			cprint_red("[*] Connection error, please check your network, and make sure that the twtch API isn't blocked")
			return False
		json = json_parse(r.text)
		try:
			return json["data"][0]["type"] == "live"
		except IndexError:
			#If the streamer is offline, then the data section of the dict will be empty
			#so it will cause an index error
			return False

def make_streamers( ):
	return [Streamer(name) for name in open("streamers.txt", "r").readlines()]

def main( ):
	#this makes a list of 'streamer' objects
	Streamers = make_streamers( )
	parser = parse_arguments( )
	print(parser)
	while True:
		for Streamer in Streamers:
			if Streamer.is_online( ): 
				cprint_green("Streamer {} is online".format(Streamer.name))
				Streamer.last_test = True
			else:
				#if the last ping on the streamer was live, and then they go offline, download the vod.
				if Streamer.last_test==True:
					cprint_green("Streamer {} has just gone offline, now downloading VOD".format(Streamer.name))

				Streamer.last_test = False
		time.sleep(10) #sleep for 10 seconds every iteration

if __name__=="__main__":
	main( )





