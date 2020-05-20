from typing import List
import json


class Account:

    """
    Account Model
    """

    def __init__(self,identifier,name):

        self.id = identifier
        self.name =  name

    def to_dict(self):
        return{"id":self.id,"name":self.name}

    def get_balance(self):

        with open("ledger.json", "r") as file:
            ledger = json.load(file)
            debit = sum([entry['debit'] for entry in ledger if entry['account'] == self.id ])
            credit = sum([entry['credit'] for entry in ledger if entry['account'] == self.id ])

        print(f"Balance Account {self.name}: {credit- debit}")


class Transaction:

    """
    One transaction will book into two accounts: one debit & one time credit
    """

    def __init__(self,id,account_debit:Account,amount_debit:float,account_credit:Account,amount_credit:float):
        self.id = id
        self.account_debit = account_debit
        self.amount_debit =  amount_debit


        self.account_credit = account_credit
        self.amount_credit = amount_credit
        
    def validate(self):

        if not self.amount_debit == self.amount_debit:
            raise Exception('Amount for debit and credit are not the same')

    def book(self):
        return [{ "id": self.id,
                "account" : self.account_debit.id,
                "debit":self.amount_debit,
                "credit": 0},
                { "id": self.id,
                "account":self.account_credit.id,
                "debit":0,
                "credit":self.amount_credit
                }
                ]


class BookingJournalLedger:

    """
    Booking Ledger... not exactly as in the datamodel that I presented
    """


    def __init__(self,transaction:Transaction):

        self.transaction = transaction
  
    def get_ledger(self):
        
        with open("ledger.json", "r") as file:
        
            ledger_list = json.load(file)
            ledger = [entry for entry in ledger_list]
        return ledger

    def update_ledger(self,ledger_list = List[Transaction]):


        with open("ledger.json", "w") as file:
            json.dump(ledger_list, file)
    
    def book_transaction(self):
        
        # validate that the transaction is correct 
    
        self.transaction.validate()
        ledger = self.get_ledger()

        updatedledger= ledger + self.transaction.book()

        self.update_ledger(updatedledger)
        

