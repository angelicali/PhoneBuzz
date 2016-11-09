from flask import Flask, request
import twilio.twiml
from twilio.util import RequestValidator


auth_token = "2e0586523d70a82d17d94c2f23c45d51"

validator = RequestValidator(auth_token)

url = "https://phonebuzz-yl.herokuapp.com/"

app = Flask(__name__)

def validate_twilio(d):
	pass


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
		resp.say("request form has "+str(info))
		val = request.values
		resp.say("request values have " + str(val))

		if 'Digits' in request.values:
			num = request.values['Digits']
			resp.say(allfizzbuzz(int(num)))
		

	with resp.gather(timeout=5) as gather:
		gather.say('Enter a number to play the phone buzz game')

	resp.redirect('/')

	return str(resp)



if __name__ == "__main__":
	app.run(debug=True)

