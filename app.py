from flask import Flask, render_template
from TarponAlgo import fetch_price_and_iv, find_best_strikes
app = Flask(__name__)

@app.route('/')
def index():
    symbols = ['^SPX', 'XSP']
    days_to_expiration = 1
    results = []

    for symbol in symbols:
        try:
            S, iv = fetch_price_and_iv(symbol)
            if iv is None:
                results.append(f"Could not fetch IV for {symbol}")
                continue

            lower_short_strike, upper_short_strike = find_best_strikes(S, iv, days_to_expiration)
            results.append({
                'symbol': symbol,
                'current_price': round(S, 2),
                'implied_volatility': round(iv, 2),
                'lower_short_strike': round(lower_short_strike, 2),
                'upper_short_strike': round(upper_short_strike, 2)
            })
        except Exception as e:
            results.append(f"Error fetching data for {symbol}: {e}")
    return render_template('index.html', results=results)
if __name__ == "__main__":
    app.run(debug=True)
