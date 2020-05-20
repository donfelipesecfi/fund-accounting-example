"""
Example of how the double entry booking system can work for our case
"""
import json
from models import Account, Transaction, BookingJournalLedger 
from helper import empty_ledger
# just to run the script...
# empty the ledger first
empty_ledger()



# Assume we start up a new fund, and we find an investor who gives up 100 USD
# given that we have an double entry book keeping system we need to  book this amount
# to do that. we first need to create an account for the investor and an account for the cash

cash_account = Account(identifier=1,name='USD Cash Account')
investor_account = Account(identifier=2,name='Investor 1 Account')

# then we create book create the pre-booking to these accounts

transaction_1 = Transaction(id=1,
                 account_credit=cash_account,
                 amount_credit=100,
                 account_debit=investor_account,
                 amount_debit=100)

# if we are sure that we have selected the right accounts, we book the transaction into the journal ledger

booking_1 = BookingJournalLedger(transaction=transaction_1)
booking_1.book_transaction()

# the first client comes in - asks for money and he gets it
# to book this transaction, we have to know to which accounts we want to add these transactions
# plus we need to create these accounts

loan_account_1 = Account(identifier=3,name='Loan given to Client 1')
equity_account_1 = Account(identifier=4,name='Equity from Client 1')

# we first book the loan which is payed from the cash account, thus we have. 
# we dont book this yet...
transaction_2 = Transaction(id=2,
                 account_credit=loan_account_1,
                 amount_credit=50,
                 account_debit=cash_account,
                 amount_debit=50)

# aand the equity.... since this will generate some windfall profits (because we need to book a value into our system), 
# but need a different account to book this transaction too (remember double entry book keeping)
# we will therefore create another account of "unrealized profits" from equity

unreal_equity_account = Account(identifier=5,name='Unrealized Equity Gains')

# thus we have found a place to live for the unrealized gains
# now, lets define the transaction

transaction_3 = Transaction(id=3,
                 account_credit=equity_account_1,
                 amount_credit=10,
                 account_debit=unreal_equity_account,
                 amount_debit=10)

# lets log all these transactions

BookingJournalLedger(transaction=transaction_2).book_transaction()
BookingJournalLedger(transaction=transaction_3).book_transaction()



## WHY ALL THIS ACCOUNTING SHIT? well.. because now its super easy to retrieve the data!

#these are the asset accounts
print("ASSETS\n")
cash_account.get_balance()
loan_account_1.get_balance()
equity_account_1.get_balance()


# these accounts would be on the liability side of the balance sheet. thus their balance will be negative most of the times.
print("\n\nLIABILITIES\n")
unreal_equity_account.get_balance()
investor_account.get_balance()


# if we would have this in a database with a date time field, we could filter for differnt time horizons
# and easily determine the perfomance just by comparing the balances between two points in time






