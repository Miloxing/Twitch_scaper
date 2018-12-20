import time
import requests
import argparse
from json import loads as json_parse
from requests.exceptions import RequestException
from color import cprint_red, cprint_blue, cprint_green

TWITCH_LINK = "https://www.twitch.tv/"
API_LINK 	= "https://api.twitch.tv/"
CLIENT_ID   = "owpia6t4yoo37fxnq372oq39jzauon"
REPEAT_TIME = 60

def parse_arguments( ):
	parser = argparse.ArgumentParser(description="Twtich scraper")
	parser.add_argument("-v","--verbosity", help="Verbosity level of debugging (1-3)", type=int, required=False)
	parser.add_argument("-f", "--file", help="Path to file of streamers to scrape", 
						type=str, required=True, default="streamers.txt")

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

	def make_request(self,url):
		try:
			r = requests.get(url, headers={"Client-id": CLIENT_ID})
		except RequestException:
			cprint_red("Bad internet detected, exiting program")
		return json_parse(r.text)

	def is_online(self):
		cprint_green("[*] Checking if streamer {} is online".format(self.name))
		url = "{}/helix/streams?user_login={}".format(API_LINK, self.login)
		json = self.make_request( )
		return json.get("data", ["a"])[0].get("type", False) == "live" #this shit is retarded

	def latest_vod(self):
		url = "{}kraken/channels/{}/videos".format(API_LINK, TWITCH_LINK)
		json = self.make_request(url)
		return json.get("videos", [False])[0]

	def download_vod(self, filename, url):
		cprint_green("Downloading vod for {}".format(url))
		chunk_size = 1024
		try:
			r = requests.get(url, stream=True)
		except RequestException as e:
			cprint_red("Could not open URL: {}".format(url))
		with open(filename+".mp4", "wb") as f:
			for chunk in r.iter_content(chunk_size=chunk_size):
				if not chunk:
					continue
				f.write(chunck)
				f.flush( )
		cprint_green("File downloaded succesfully, at filename: {}.mp4".format(filename))
		subprocess.run('rclone move {} milo:milo/b/Twitch/{}'.format(filename,self.name))
		return True

def make_streamers(file="streamers.txt"):
	return [Streamer(name) for name in open(file, "r").readlines()]

def main( ):
	#this makes a list of 'streamer' objects
	try:
		parser = vars(parse_arguments( ))
		Streamers = make_streamers(parser["file"])
		while True:
			for Streamer in Streamers:
				if Streamer.is_online( ): 
					cprint_green("Streamer {} is online".format(Streamer.name))
					Streamer.last_test = True
				else:
					#if the last ping on the streamer was live, and then they go offline, download the vod.
					if Streamer.last_test:
						cprint_green("Streamer {} has just gone offline, now downloading VOD".format(Streamer.name))
						vod = Streamer.latest_vod( )
						Streamer.download_vod("{}_{}_{}".format(Streamer.name, vod["created_at"], vod["game"]))
					Streamer.last_test = False
			#This would be 
			time.sleep(REPEAT_TIME) 
	except KeyboardInterrupt:
		cprint_green("Exitting the program")
if __name__=="__main__":
	main( )
