from flask import Flask, request
import twilio.twiml
from twilio.util import RequestValidator

from hashlib import sha1
import hmac 



auth_token = "2e0586523d70a82d17d94c2f23c45d51"
validator = RequestValidator(auth_token)
url = "https://phonebuzz-yl.herokuapp.com/"


app = Flask(__name__)

def hash_url(url_params):
	global auth_token
	hashed = hmac.new(auth_token, url_params, sha1)
	return hashed.digest().encode("base64").rstrip('\n')
	

def validate_twilio(d):
	keys = sorted(list(d))
	params =  ''.join( [ key + d[key] for key in keys] )
	url_with_params = url + params
	signature = hash_url(url_with_params)
	print(signature)
	return validator.validate(url,d,signature)
		


def fizzbuzz(n):
	if n%3==0 and n%5==0:
		return "fizz buzz" 
	elif n%3==0:
		return "fizz"
	elif n%5==0:
		return "buzz"
	else:
		return str(n)
	
def allfizzbuzz(n):
	return ' '.join([fizzbuzz(i) for i in range(1,n+1)])



@app.route("/", methods=['GET','POST'])
def hello():
	resp = twilio.twiml.Response()

	if request.method == 'POST':
		info = request.form
		if validate_twilio(info):
			resp.say("Comfirmed to have come from twilio")
		else:
			resp.say("NOT VALID!!")
		if 'Digits' in request.values:
			num = request.values['Digits']
			resp.say(allfizzbuzz(int(num)))
		

	with resp.gather(timeout=5) as gather:
		gather.say('Enter a number to play the phone buzz game')

	resp.redirect('/')

	return str(resp)



if __name__ == "__main__":
	app.run(debug=True)
	#print(validate_twilio(test_d))

