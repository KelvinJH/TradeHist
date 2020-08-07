import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


scope = config.scope
creds = ServiceAccountCredentials.from_json_keyfile_name('./goog_secretclient.json', scope)
client = gspread.authorize(creds)

sheet1 = client.open('IRA').sheet1

results = sheet1.get_all_records()


current_rows = len(sheet1.get_all_values())
print(current_rows)

class Writer:

	#Cells A(ROW):F(ROW)
	def writeOptionInfo(self, symbol, open_date, exp_date, order_type, action, curr_price):
		range = self.locateCells(1)
		sheet1.update(range, [[symbol, open_date, exp_date, order_type, action, curr_price]])


	#Cells J(ROW):L(ROW)
	def writeTransactionCost(self, strike, cost, count):
		range = self.locateCells(2)
		sheet1.update(range, [[strike, cost, count]])


	#Cells P(ROW):R(ROW) & W(ROW):X(ROW)
	def writeClosingInfo(self, fees, exit_price, close_date):
		ranges = self.locateCells(3)
		sheet1.update(ranges[0], [[' ' , fees, exit_price, close_date]])
		sheet1.update(ranges[1], [['Close', 'TD']])	



	def findStrike(self, option, strike):
		if option == 'CALL':
			chunks = strike.split('C')
			return chunks[len(chunks)-1]
		else:
			chunks = strike.split('P')
			return chunks[len(chunks)-1]

	def locateCells(self, section):

		#locate empty space for option info
		emptyRow = str(current_rows + 1)
		if section == 1:
			cellRange = 'A' + emptyRow + ':F' + emptyRow
			return cellRange

		#locate empty space for transaction info	
		elif section == 2:
			cellRange = 'J' + emptyRow + ':L' + emptyRow
			return cellRange

		#locate empty space for closing info
		else:
			cellRange1 = 'O' + emptyRow + ':R' + emptyRow
			cellRange2 = 'W' + emptyRow + ':X' + emptyRow
			return cellRange1, cellRange2












