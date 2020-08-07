from tda import auth, client
import json
import config
from datetime import datetime, date
from pprint import pprint
from report import Writer



googSheets = Writer()
today = date.today()
startDate = date(today.year, today.month - 1, 20)


try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(config.executable_path) as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)

response = c.get_transactions(config.ira_account, transaction_type=c.Transactions.TransactionType.TRADE, start_date=startDate)
assert response.ok, response.raise_for_status()
trades = response.json()
# print(json.dumps(trades, indent=4))

# NEED FOR TRANSACTION INFO: symbol, open_date, exp_date, type, action, curr_price
# NEED FOR COST INFO: strike, cost, count
# NEED FOR CLOSING INFO: fees, exit_price, close_date


#figured out how to get data and store data

tradeCost = 0.0
for x in range(len(trades)-1, -1, -1):
	trade = trades[x]

	#Used to confirm trade is an OPTION before proceeding
	if trade['transactionItem']['instrument']['assetType'] != 'OPTION':
		continue

	tradeCost += trade['netAmount']
	fees = trade['fees']
	transaction = trade['transactionItem']

	if transaction['instruction'] == 'BUY':
		transactionData = {
			'symbol': transaction['instrument']['underlyingSymbol'],
			'openDate': trade['orderDate'].split('T')[0],
			'expDate': transaction['instrument']['optionExpirationDate'].split('T')[0],
			'type': transaction['instrument']['putCall'],
			'currentPrice': 0.0
		}
		transactionData.update({'currentPrice': c.get_quote(transactionData['symbol']).json()[transactionData['symbol']]['lastPrice']})	
		
		costData = {
			'strike': googSheets.findStrike(transactionData['type'], transaction['instrument']['symbol']),
			'cost': transaction['price'],
			'count': transaction['amount']
		}

		googSheets.writeOptionInfo(transactionData['symbol'], 
								transactionData['openDate'], 
								transactionData['expDate'],
								transactionData['type'],
								transaction['instruction'], 
								transactionData['currentPrice'])

		googSheets.writeTransactionCost(costData['strike'], costData['cost'], costData['count'])

	elif transaction['instruction'] == 'SELL':
		closingData = {
			'totalFees': fees['commission'] + fees['regFee'],
			'exitPrice': transaction['price'],
			'closeDate': trade['orderDate'].split('T')[0]
		}
		googSheets.writeClosingInfo(closingData['totalFees'], closingData['exitPrice'], closingData['closeDate'])

	# pprint(trade)
	# print("Total fees paid for {tradeEffect} the trade was {totalFees}".format(**transactionData))








