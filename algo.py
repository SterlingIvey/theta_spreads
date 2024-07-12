from flask import Flask, render_template
import yfinance as yf
import numpy as np

def fetch_price_and_iv(symbol):
    if symbol == '^SPX':
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        current_price = hist['Close'].iloc[-1]
        
        # Fetch VIX data for SPX as a measure of implied volatility
        vix_ticker = yf.Ticker("^VIX")
        vix_hist = vix_ticker.history(period="1d")
        implied_volatility = vix_hist['Close'].iloc[-1] / 100 # VIX is in percentage

    elif symbol == 'XSP':
        ticker = yf.Ticker('^SPX')
        hist = ticker.history(period="1d")
        current_price = hist['Close'].iloc[-1] / 10 # XSP is 1/10th of SPX

        # Fetch VIX data for SPX as a measure of implied volatility
        vix_ticker = yf.Ticker("^VIX")
        vix_hist = vix_ticker.history(period="1d")
        implied_volatility = vix_hist['Close'].iloc[-1] / 100 # VIX is in percentage
    
    else:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        current_price = hist['Close'].iloc[-1]
        implied_volatility = None # Handle other symbols as needed

    return current_price, implied_volatility

def calculate_standard_deviation(iv, days_to_expiration, underlying_price):
    std_dev = (iv / np.sqrt(256)) * np.sqrt(days_to_expiration) * underlying_price
    return std_dev

def find_best_strikes(S, iv, T):
    # S: current stock price
    # iv: implied volatility
    # T: time to expiration in days

    std_dev = calculate_standard_deviation(iv, T, S)
    upper_short_strike = S + std_dev
    lower_short_strike = S - std_dev

    return lower_short_strike, upper_short_strike

def main():
    symbol = '^SPX'
    days_to_expiration = 1

    try:
        S, iv = fetch_price_and_iv(symbol)
        if iv is None:
            print(f"Could not fetch IV for {symbol}")
            return
        
        lower_short_strike, upper_short_strike = find_best_strikes(S, iv, days_to_expiration)
        print(f"Symbol: {symbol}")
        print(f"Current Price: ${S}")
        print(f"Implied Volatility (VIX for SPX): {iv * 100:.2f}")
        print(f"Lower Short Strike: ${lower_short_strike}")
        print(f"Upper Short Strike: ${upper_short_strike}")

    except Exception as e:
        print(f"Error fetching data or calculating strikes: {e}")

if __name__ == '__main__':
    main()
