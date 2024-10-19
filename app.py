from flask import Flask, render_template, request
import phonenumbers
from phonenumbers import geocoder, carrier
import requests  # For calling NumVerify API

app = Flask(__name__)

# Replace with your actual API key from NumVerify
NUMVERIFY_API_KEY = '39da3e897576d505bbd3bc9ec8737727'

def get_phone_number_details(phone_number):
    try:
        # Parse the phone number using phonenumbers library
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.country_name_for_number(parsed_number, "en")
        sim_carrier = carrier.name_for_number(parsed_number, "en")

        # Call NumVerify API for more details
        numverify_url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone_number}"
        response = requests.get(numverify_url)
        data = response.json()

        if not data.get('valid'):
            return {"Error": "Invalid phone number"}

        state = data.get('location', 'Not Available')
        return {
            "Phone Number": phone_number,
            "Country": country,
            "State": state,
            "Carrier": sim_carrier or "Not Available"
        }

    except phonenumbers.NumberParseException as e:
        return {"Error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def home():
    details = None
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        details = get_phone_number_details(phone_number)

    return render_template('index.html', details=details)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
