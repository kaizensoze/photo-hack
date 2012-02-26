
import json
import pprint
import requests
import unicodedata

token = "27c3ebe3da766d8b88f9dec8147266e1c4db89b25ccfbc77c9ed8c64ccfbbac6"

headers = {
    "Authorization": "OAuth %s" % (token)
}

# create stream
r = requests.get("http://public-api.piictu.com/v2/streams/new", headers=headers)
res = json.loads(r.text)
#print(json.dumps(res, indent=4))

photo_id = res["photo_id"]
s3_params = res["s3_params"]
access_key = s3_params["access_key"]
key = s3_params["key"]
policy = s3_params["policy"]
signature = s3_params["signature"]
sas = s3_params["sas"]
bucket = s3_params["bucket"]


# upload image to S3
data = {
    "key": key,
    "AWSAccessKeyId": access_key,
    "acl": "public-read",
    "policy": policy,
    "signature": signature,
    "success_action_status": sas,
    "Content-Type": "image/jpeg",
    "file": "BLAH" #"http://dev.ragemyface.com/uploaded_images/u1330270167.jpeg"
}

for k,v in data.iteritems():
    if not isinstance(v, str):
        data[k] = unicodedata.normalize('NFKD', v).encode('ascii', 'ignore')

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)

url = "http://%s.s3.amazonaws.com" % (bucket)
r = requests.post(url, data=data)
print(r.text)

