
from hordak.models import Account
from fund_accounting_app.models import FundManager
from decimal import Decimal

class CreateNewFundManager:


    def __init__(self, name: str,fund:str,hurdle:Decimal,amount:int,currencies: List[str] = ["USD"])-> None:
        """[summary]

        Arguments:
            name {str} -- name of fund manager/ fund
            fund {str} -- fund uuid 
            hurdle {Decimal} -- hurdle
            amount {int} -- amount of stake
        """
        self.name = name
        self.fund = fund
        self.amount = amount
        self.hurdle = hurdle
        self.currencies = currencies
        

    def _create_accounts(self):
        
        account = Account(name=self.name,type=Account.TYPE.equity).save()
        
        cash_account = Account()

        fund_manager = FundManager(name=self.name,account=account,hurdle=self.hurdle)
        fund_manager.save()


        return account, fund_manager, fund_manager_cash_account
        
    def _book_transaction(self,account,):





