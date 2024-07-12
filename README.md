# theta_spreads

 I built this tool to visualize and automate calculations for selling iron condors and credit spreads. Through scraping from yfinance, it pulls the yesterday's (or today's if after 4:00 PM EST) prices of SPX and XSP. It also pulls current price of the VIX. This is expressed in 'Implied Volatility' on the dashboard.

It plugs in those numbers to calculate the ideal short strike prices, then lists them on the dashboard. The underlying calculation is a formula from Dan Passarelli's Trading Options Greeks. I think it's on page 198. I highly recommend that book if you're interested in theta decay strategies. 

I want to keep this project very small in scope and not ambitious, as I will maintain it myself and don't want it to get stale or overwhelming. It's a tool; not too flashy or impressive. It simply automates something that makes my life a lot easier and better. 
