import requests
import json
import datetime

class BankAccount(object):

    def __init__(self, amount):
        if amount < 0:
            raise ValueError("Amount can not be negative")
        self.amount = amount
        self.transactions = []
        
    def deposit(self, value):
        """
        Add funds to bank account
        """
        if value < 0:
            raise ValueError("Value can not be negative")
        self.transactions.append(Transaction(self.amount, self.amount+value))
        self.amount += value
        return self.amount
    
    def withdraw(self, value):
        """
        Withdraw funds from bank account
        """
        if value < 0:
            raise ValueError("Value can not be negative")
        elif value > self.amount:
            raise ValueError("Not enough funds")
        self.transactions.append(Transaction(self.amount, self.amount-value))
        self.amount-=value        
        return self.amount
    
    def get_amount(self):
        """
        Return current saldo
        """
        return self.amount
    
    def get_transaction_history(self):
        """
        Return list of transactions
        """
        return self.transactions


class Transaction(object):
    IP_SERVICE_REQUEST_URL = "http://jsonplaceholder.typicode.com/posts/1"
    
    def __init__(self, initial_amount, final_amount):
        self.user_id = self._get_id()
        self.timestamp = datetime.datetime.now()
        self.initial_amount = initial_amount
        self.final_amount = final_amount
        self.difference = final_amount - initial_amount
        
    def _get_id(self):
        """
        Make a http request to third party web service in order to get current ip address
        """
        resp = requests.get(self.IP_SERVICE_REQUEST_URL)
        if not resp.status_code == 200:
            raise Exception("Can not obtain IP address")
        return json.loads(resp.content)["userId"]
    
    def __str__(self):
        return "    ".join(map(str,[self.timestamp, 
                                  self.user_id, 
                                  self.initial_amount, 
                                  self.final_amount,
                                  self.difference]))

def add_to_bank_account(account):
    while True:
        try:
            amount = raw_input("How much funds you would like to add? ")
            account.deposit(int(amount))
        except ValueError as e:
            print(e)
            continue
        else:
            break
    print("Your account saldo is %s"%account.get_amount())

def withdraw_from_bank_account(account):
    while True:
        try:
            amount = raw_input("How much funds you would like to withdraw? ")
            account.withdraw(int(amount))
        except ValueError as e:
            print(e)
            continue
        else:
            break
    print("Your account saldo is %s"%account.get_amount())

def get_transaction_history(account):
    if account.get_transaction_history():
        print("ID   Timestamp    user Id  initial amount  final amount    difference")
        for i, tr in enumerate(account.get_transaction_history()):
            print(str(i+1)+"   "+str(tr))
    else:
        print("No transactions found")

if __name__ == "__main__":

    options = {
        "1": add_to_bank_account,
        "2": withdraw_from_bank_account,
        "3": get_transaction_history
    }

    while True:
        try:
            amount = int(raw_input("How much funds you have on your bank account? "))
        except ValueError:
            print("Should be a number!")
            continue
        else:
            try:
                b = BankAccount(amount)
            except ValueError as e:
                print(e)
                continue
            break

    while True:
        choice = raw_input("""
What would you like to do? 
%s
Press any other key to exit
    """%"".join(['{0}: {1}\n'.format(k,v.__name__) for k,v in options.iteritems()]))

        if choice in options.keys():
            options[choice](b)
        else:
            break
