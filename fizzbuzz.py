from flask import Flask
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello():
	resp = twilio.twiml.Response()
	resp.say("Hello Monkey!" , voice="alice")

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)

