import json
import requests

def getVenues(gps_loc):
	lat = gps_loc[0]
	lng = gps_loc[1]
	limit = 10
	token = "KDGVWHX0HBPV0MPJHD1U3JK5LBX0TNEV2IJPVL0HQFOXZKAE"
	version = "20120223"
	
	url = "https://api.foursquare.com/v2/venues/search?ll=%s,%s&limit=%s&oauth_token=%s&v=%s" % (lat, lng, limit, token, version)
	r = requests.get(url)
	venues_raw = json.loads(r.content)["response"]["venues"]
	
	# check results
	#print(json.dumps(venues_raw, indent=4))
	
	# return venues with subset of info
	venues = []
	for v in venues_raw:
		v_temp = {}
		v_temp["name"] = v["name"]
		v_temp["id"] = v["id"]
		v_temp["gps"] = (v["location"]["lat"], v["location"]["lng"])
		venues.append(v_temp)
	
	return venues

def getVenueStorefrontImage(venue_gps_loc):
	lat = venue_gps_loc[0]
	lng = venue_gps_loc[1]
	
	url = "http://maps.googleapis.com/maps/api/streetview?size=600x300&location=%s,%s&sensor=true" % (lat, lng)
	return url
	
	#r = requests.get(url)
	#return r.content

def main():
	input_gps_loc = (40.728672, -73.989745)
	
	venues_near_input = getVenues(input_gps_loc)
	
	for venue in venues_near_input:
		venue_img = getVenueStorefrontImage(venue["gps"])
		venue["img"] = venue_img
		
	return venues_near_input

if __name__ == "__main__":
    venues_json = main()
    print(venues_json)

