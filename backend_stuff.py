import json
import requests

def getVenues(gps_loc):
    lat = gps_loc[0]
    lng = gps_loc[1]
    limit = 2
    token = "KDGVWHX0HBPV0MPJHD1U3JK5LBX0TNEV2IJPVL0HQFOXZKAE"
    version = "20120223"
    
    url = "https://api.foursquare.com/v2/venues/search?ll=%s,%s&limit=%s&oauth_token=%s&v=%s" % (lat, lng, limit, token, version)
    r = requests.get(url)
    venues_raw = json.loads(r.content)["response"]["venues"]

    # check results
    print(json.dumps(venues_raw, indent=4))

    # return venues with subset of info
    venues = []
    for v in venues_raw:
        v_temp = {}
        v_temp["name"] = v["name"]
        v_temp["id"] = v["id"]
        v_temp["gps"] = (v["location"]["lat"], v["location"]["lng"])
        v_temp["address"] = v["location"]["address"] + ", " + v["location"]["city"] + ", " + v["location"]["state"]
        v_temp["categories"] = [c["name"] for c in v["categories"]]
        venues.append(v_temp)

    return venues

def getVenueStorefrontImage(venue):
    url = "http://maps.googleapis.com/maps/api/streetview?size=600x300&location=%s&sensor=true" % (venue["address"])
    r = requests.get(url)
    img_data = r.content

    outfile = file("compare_images/%s.jpeg" % (venue["id"]), 'wb')
    outfile.write(img_data)
    outfile.close()

def findMatch(venue):
    return None

def main(image_name, lat_lng):
    #input_gps_loc = (40.728672, -73.989745)

    # get all venues near gps coords of user's device
    venues_near_input = getVenues(lat_lng)

    # get storefront images of all nearby venues and store on disk
    for venue in venues_near_input:
        getVenueStorefrontImage(venue)

    # take uploaded image, compare against storefront images, and find a match
    match = findMatch()

if __name__ == "__main__":
    venues_json = main()
    print(venues_json)
