from flask import Flask, request, render_template
import twilio.twiml
from twilio.util import RequestValidator
from twilio.rest.lookups import TwilioLookupsClient
from twilio.rest import TwilioRestClient

from hashlib import sha1
import hmac 


account_sid = "ACbba02f681a40e42defdc0ae3c7cd0acd"
auth_token = "2e0586523d70a82d17d94c2f23c45d51"
validator = RequestValidator(auth_token)
default_url = "https://phonebuzz-yl.herokuapp.com/"




app = Flask(__name__)

def hash_url(url_params):
	# hash url into twilio signature
	global auth_token
	hashed = hmac.new(auth_token, url_params, sha1)
	return hashed.digest().encode("base64").rstrip('\n')

def validate_twilio(url,d):
	# check if incoming call is validate
	keys = sorted(list(d))
	params =  ''.join( [ key + d[key] for key in keys] )
	url_with_params = url + params
	signature = hash_url(url_with_params)
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

def valid_phone_number(num_str):
	client = TwilioLookupsClient(account=account_sid, token=auth_token)
	try:
		number = client.phone_numbers.get(num_str)
		number = number.phone_number  
		return number
	except:
		return None


@app.route("/", methods=['GET','POST'])
def dialPhoneBuzz():
	if request.method == 'GET':
		return render_template("dial.html")
	else:
		if 'tel' in request.form:
			num = request.form['tel']
			num = valid_phone_number(num)
			if num:
				client = TwilioRestClient(account=account_sid, token=auth_token)
				# Make the call
				call = client.calls.create(to= num,  # Any phone number
								           from_="+12179797039", # Must be a valid Twilio number
								           url= defaul_url+"/fizzbuzz")
				return "Calling %s"%num
		return render_template("dial.html", error_msg = "invalid phone number")




@app.route("/fizzbuzz", methods=['GET','POST'])
def phoneBuzz():
	resp = twilio.twiml.Response()
	if request.method == 'POST':
		info = request.form
		if validate_twilio(default_url+"/fizzbuzz", info):
			if 'Digits' in request.values:
				num = request.values['Digits']
				resp.say(allfizzbuzz(int(num)))
			else:
				resp.say("NOT VALID. Ending phone call.")
				return str(resp)
		

	with resp.gather(timeout=4) as gather:
		gather.say('Enter a number to play the phone buzz game. ')

	resp.redirect('/fizzbuzz')

	return str(resp)






if __name__ == "__main__":
	app.run(debug=True)

