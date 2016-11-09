from flask import Flask, request
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello():
	resp = twilio.twiml.Response()
	
	if 'Digits' in request.values:
		num = request.values['Digits']
		
		resp.say('You entered '+str(num))


	with resp.gather(numDigits=1) as gather:
		gather.say('Enter a number')

	resp.redirect('/')

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)

