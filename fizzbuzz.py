from flask import Flask, request
import twilio.twiml

app = Flask(__name__)




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
	return ' '.join([fizzbuzz(i) for i in range(1,i+1)])


@app.route("/", methods=['GET','POST'])
def hello():
	resp = twilio.twiml.Response()
	
	if 'Digits' in request.values:
		num = request.values['Digits']
		
		resp.say(allfizzbuzz(int(num)))


	with resp.gather(timeout=5) as gather:
		gather.say('Enter a number to play the phone buzz game')

	resp.redirect('/')

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)

