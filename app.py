from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "YOUR_CURRENCYFREAKS_API_KEY"  # get this from CurrencyFreaks dashboard
BASE_URL = "https://api.currencyfreaks.com/v2.0"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/currencies')
def get_currencies():
    url = f"{BASE_URL}/supported-currencies?apikey={API_KEY}"
    resp = requests.get(url).json()
    # resp["supportedCurrenciesMap"] holds mapping of codes to details
    return jsonify(resp["supportedCurrenciesMap"])

@app.route('/convert', methods=['GET'])
def convert_currency():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = request.args.get('amount', type=float)
    if not from_currency or not to_currency or amount is None:
        return jsonify({"error": "Please provide 'from', 'to', and 'amount' parameters."}), 400

    url = f"{BASE_URL}/rates/latest?apikey={API_KEY}&symbols={to_currency}&base={from_currency}"
    resp = requests.get(url).json()
    if "rates" not in resp or to_currency not in resp["rates"]:
        return jsonify({"error": "Invalid currency code or API error."}), 400

    rate = float(resp["rates"][to_currency])
    converted_amount = round(rate * amount, 2)
    return jsonify({
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount,
        "converted_amount": converted_amount,
        "rate": round(rate, 6)
    })

if __name__ == "__main__":
    app.run(debug=True)
