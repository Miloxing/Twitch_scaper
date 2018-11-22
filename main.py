import requests
from json import loads as json_parse

TWITCH_LINK = "https://www.twitch.tv/"
API_LINK 	= "https://api.twitch.tv/"
CLIENT_ID   = "owpia6t4yoo37fxnq372oq39jzauon"

def make_dictionary( ):
	return {
		streamer.rstrip() : {
			"username": streamer.lower().rstrip(),
			"link": "{}{}".format(TWITCH_LINK, streamer.lower()).rstrip()
		} for streamer in open("streamers.txt", "r").readlines()
	}


def is_online( streamer ):
	print("[*] checking if streamer {} is online".format(streamer["username"]))
	r = requests.get(API_LINK+"/helix/streams?user_login={}".format(streamer["username"]), headers={
		"Client-id": CLIENT_ID
	})
	json_load = json_parse(r.text)
	try:
		return json_load["data"][0]["type"] == "live"
	except IndexError:
		#If the streamer is offline, then the data section of the dict will be empty
		#so it will cause an index error
		return False



def main( ):
	print(check_online({"username": "imaqtpie"}))

if __name__=="__main__":
	main( )