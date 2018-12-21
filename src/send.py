from datetime import datetime, tzinfo, timedelta
from email.utils import formatdate

from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 

import requests

users = []
domain = 'uldocs.atilf.fr'

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)

def sign_data(private_key_loc, data):
    '''
    param: private_key_loc Path to your private key
    param: package Data to be signed
    return: base64 encoded signature
    '''
    key = open(private_key_loc, "r").read() 
    rsakey = RSA.importKey(key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    # It's being assumed the data is base64 encoded, so it's decoded before updating the digest 
    # digest.update(b64decode(data)) 
    digest.update(data) 
    sign = signer.sign(digest) 
    return b64encode(sign)



def sendMsg(txt, msgid, sender):
	print("sending msg...")
	tgturl = "mastodon.etalab.gouv.fr"
	tgtbox = "/users/cerisara/inbox"
	dat = datetime.utcnow().replace(tzinfo=simple_utc()).isoformat()
	s = '{ "@context": "https://www.w3.org/ns/activitystreams", \
"id": "https://'+domain+'/nanoAP/msgs/create-'+msgid+'", \
"type": "Create", \
"actor": "https://'+domain+'/nanoAP/users/'+sender+'.json", \
"object": { "id": "https://'+domain+'/nanoAP/msgs/'+msgid+'", \
"type": "Note", \
"published": "'+dat+'", \
"attributedTo": "https://'+domain+'/nanoAP/users/'+sender+'.json", \
"inReplyTo": "", \
"content": "'+txt+'", \
"to": "https://www.w3.org/ns/activitystreams#Public" \
}}'
	print("string",s)
	dathtml = formatdate(timeval=None, localtime=False, usegmt=True)
	print("dathtml",dathtml)
	tobesigned = "(request-target): post "+tgtbox+'\nhost: '+tgturl+'\ndate: '+dathtml
	print("tobesigned",tobesigned)
	signature = sign_data("private.pem", tobesigned)
	header = 'keyId="https://'+domain+'/nanoAP/users/'+sender+'.json#main-key",headers="(request-target) host date",signature="'+signature+'"'
	headers = {'Host':tgturl, 'Date':dathtml, 'Signature': header}
	print("headers",headers)
	print("posting...")
	r = requests.post("https://"+tgturl+tgtbox, json=s, headers=headers)
	print("post response ",r)

sendMsg("msg de toto","toto1","pers1")


