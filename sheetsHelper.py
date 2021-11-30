from oauth2client.service_account import ServiceAccountCredentials
import gspread
from pprint import pprint



class Writer:

	def __init__(self): 
		gc = gspread.service_account(filename='credentials.json')
		sh = gc.open_by_key('1vU4fP-Y-ZiOeuLGbKwQvJTIPfBKHM9RzLKad3a_yTuA')
		self.worksheet = sh.sheet1
		res = self.worksheet.get_all_values()
		self.current_rows = len(res)


	def printAll(self):
		pprint(self.worksheet.get_all_records())
		print(self.current_rows)

	#Cells A(ROW):F(ROW)
	def writeOptionInfo(self, symbol, open_date, exp_date, order_type, action, curr_price):
		range = self.locateCells(1)
		self.worksheet.update(range, [[symbol, open_date, exp_date, order_type, action, curr_price]])


	#Cells J(ROW):L(ROW)
	def writeTransactionCost(self, strike, cost, count):
		range = self.locateCells(2)
		self.worksheet.update(range, [[strike, cost, count]])


	#Cells P(ROW):R(ROW) & W(ROW):X(ROW)
	def writeClosingInfo(self, fees, exit_price, close_date):
		ranges = self.locateCells(3)
		self.worksheet.update(ranges[0], [[' ' , fees, exit_price, close_date]])
		self.worksheet.update(ranges[1], [['Close', 'TD']])	



	def findStrike(self, option, strike):
		if option == 'CALL':
			chunks = strike.split('C')
			return chunks[len(chunks)-1]
		else:
			chunks = strike.split('P')
			return chunks[len(chunks)-1]

	def locateCells(self, section):

		#locate empty space for option info
		emptyRow = str(self.current_rows + 1)
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








