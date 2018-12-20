from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response

app = Flask(__name__)
# app = Flask("nanoAP")
users = []
domain = 'uldocs.atilf.fr'

def setup_app(app):
	global users
	# All initialization code
	with open("users.txt") as f: lines=f.readlines()
	users = [s.strip() for s in lines]
	print("nusers "+str(len(users)))

@app.route('/')
def users():
	# request.url for the full URL
	# request.args.get('resource') for argument resource
	# parms = request.query_string
	print("got user request ")
	# user = str(request.url)
	# i = user.find('/nanoAP/users/')
	# user=user[i+14:]
	return "not implemented"

@app.route('/.well-known/<cmd>')
def webfinger(cmd):
    cmd=str(cmd)
    if cmd.startswith('webfinger'):
	qs = str(request.query_string)
	i=qs.find('acct:')
	if i>=0:
		user=qs[i+5:]+'F'
		for u in users:
			if user.startswith(u):
				user=u
				break
		if user.endswith('F'): return "no such user"
		s='{ \
			"subject": "acct:'+user+'@'+domain+'", \
			"links": [ \
				{ \
					"rel": "self", \
					"type": "application/activity+json", \
					"href": "https://'+domain+'/nanoAP/users/'+user+'.json" \
				} \
			] \
		}'
		resp = make_response(s)
		resp.mimetype="application/json"
		return resp
    elif cmd.find('nodeinfo')>=0:
		s='{ \
		  "version": "0.0", \
		  "software": { \
		    "name": "nanoAP", \
		    "version": "0.0.0" \
		  }, \
		  "protocols": ["activitypub"], \
		  "services": { \
		    "inbound": [], \
		    "outbound": [] \
		  }, \
		  "openRegistrations": false, \
		  "usage": { \
		    "users": { \
		      "total": '+str(len(users))+' \
		    }, \
		    "localPosts": 0, \
		    "localComments": 0 \
		  }, \
		  "metadata": {} \
		}'
		resp = make_response(s)
		resp.mimetype="application/json"
		return resp
    return "unsupported"

# ==============================

setup_app(app)

if __name__ == '__main__':
    app.run(debug=True)


