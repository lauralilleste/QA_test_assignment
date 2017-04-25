import unittest
import app
from mock import patch
import sys
from StringIO import StringIO

class TestBankAccount(unittest.TestCase):
    
    def setUp(self):
        
        pass

    def test_create_account_successful(self):
        self.a=app.BankAccount(10)
        self.assertTrue(self.a.amount,10)
        self.assertEqual(self.a.transactions,[])
        
    def test_create_account_negative(self):
        try:
            self.a=app.BankAccount(-1)
            self.fail("ValueError was not thrown" )
        except ValueError, e:
            self.assertEquals( "Amount can not be negative", e.message )

    def test_transaction_ip_request(self):
        #somehow response.status_code != 200
        try:
            self.a=app.Transaction(2,4)
        except Exception, e:
            self.assertEquals( "Can not obtain IP address", e.message )
            self.fail("IP address could not be obtained")
            
    def test_deposit_successful(self):
        self.a=app.BankAccount(10)
        self.assertEqual(self.a.transactions,[])
        self.assertEqual(self.a.deposit(2),12)
        self.assertNotEqual(self.a.transactions,[])
        
    def test_deposit_negative(self):
        try:
            self.a=app.BankAccount(10)
            self.assertEqual(self.a.transactions,[])
            self.a.deposit(-1)
            self.fail("ValueError was not thrown" )
        except ValueError, e:
            self.assertEquals( "Value can not be negative", e.message )
            
    def test_withdraw_successful(self):
        self.a=app.BankAccount(10)
        self.assertEqual(self.a.transactions,[])
        self.assertEqual(self.a.withdraw(2),8)
        self.assertNotEqual(self.a.transactions,[])
        
    def test_withdraw_to_zero(self):
        self.a=app.BankAccount(10)
        self.assertEqual(self.a.transactions,[])
        self.assertEqual(self.a.withdraw(10),0)
        self.assertNotEqual(self.a.transactions,[])
        

    def test_withdraw_to_negative(self):
        try:
            self.a=app.BankAccount(10)
            self.assertEqual(self.a.transactions,[])
            self.a.withdraw(11)
            self.fail("ValueError was not thrown" )
        except ValueError, e:
            self.assertEquals( "Not enough funds", e.message )
            
    def test_withdraw_negative_amount(self):
        try:
            self.a=app.BankAccount(10)
            self.assertEqual(self.a.transactions,[])
            self.a.withdraw(-1)
            self.fail("ValueError was not thrown" )
        except ValueError, e:
            self.assertEquals( "Value can not be negative", e.message )      
        
    def test_get_amount(self):
        self.a=app.BankAccount(10)
        self.assertEqual(self.a.transactions,[])
        self.assertEqual(self.a.get_amount(),10)
        self.a.withdraw(8)
        self.assertEqual(self.a.get_amount(),2)
        self.a.deposit(1)
        self.assertEqual(self.a.get_amount(),3)
        self.assertNotEqual(self.a.transactions,[])
    
    def test_get_transaction_history(self):
        self.a=app.BankAccount(10)
        self.assertEqual(self.a.transactions,[])
        self.a.withdraw(8)

    def test_transaction_successful_ip(self):
        self.a=app.Transaction(2,4)
        init_timestamp=app.datetime.datetime.now()
        self.IP_SERVICE_REQUEST_URL = "http://jsonplaceholder.typicode.com/posts/1"
        response=app.requests.get(self.IP_SERVICE_REQUEST_URL)
        ip=app.json.loads(response.content)["userId"]
        self.assertEqual(self.a.user_id,ip)           
        
    def test_transaction_values(self):
        self.a=app.Transaction(2,4)
        init_timestamp=app.datetime.datetime.now()
        self.assertEqual(self.a.timestamp,init_timestamp)
        self.assertEqual(self.a.initial_amount,2)
        self.assertEqual(self.a.final_amount,4)

    def test_transaction_adding(self):
        self.a=app.Transaction(2,4)
        self.assertEqual(self.a.initial_amount,2)
        self.assertEqual(self.a.final_amount,4)
        self.assertEqual(self.a.difference,2)

    # Possible defect: 'difference' should be absolute value  
    def test_transaction_subtracting(self):
        self.a=app.Transaction(10,4)
        self.assertEqual(self.a.initial_amount,10)
        self.assertEqual(self.a.final_amount,4)
        self.assertEqual(self.a.difference,-6)

    # Possible defect: negative 'final_amount' should not be accepted
    def test_transaction_subtracting_to_negative(self):
        self.a=app.Transaction(10,-4)
        self.assertEqual(self.a.initial_amount,10)
        self.assertEqual(self.a.final_amount,-4)
        self.assertEqual(self.a.difference,-14)

    # Possible defect: transaction should not accept amounts with no difference
    def test_transaction_zero_to_zero(self):
        self.a=app.Transaction(0,0)
        self.assertEqual(self.a.initial_amount,0)
        self.assertEqual(self.a.final_amount,0)
        self.assertEqual(self.a.difference,0)
        
    def test_transaction_str(self):
        self.a=app.Transaction(4,2)
        init_timestamp=app.datetime.datetime.now()
        self.IP_SERVICE_REQUEST_URL = "http://jsonplaceholder.typicode.com/posts/1"
        response=app.requests.get(self.IP_SERVICE_REQUEST_URL)
        ip=app.json.loads(response.content)["userId"]
        self.assertEqual(self.a.user_id,ip)
        self.assertEqual(self.a.timestamp,init_timestamp)
        self.assertEqual(self.a.initial_amount,4)
        self.assertEqual(self.a.final_amount,2)
        self.assertEqual(self.a.difference,-2)
        value="    ".join(map(str,[init_timestamp,ip,4,2,-2]))
        self.assertEqual(str(self.a),value)
        
    def test_add_to_bank_account_positive(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        self.a=app.BankAccount(10)
        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda _: '3'
        app.add_to_bank_account(self.a)
        __builtins__.raw_input = original_raw_input
        self.assertEquals(sys.stdout.getvalue(),'Your account saldo is 13\n')
        
    def test_add_to_bank_account_positive(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        self.a=app.BankAccount(10)
        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda _: '3'
        app.withdraw_from_bank_account(self.a)
        __builtins__.raw_input = original_raw_input
        self.assertEquals(sys.stdout.getvalue(),'Your account saldo is 7\n')

    def test_get_transaction_history_empty(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        self.a=app.BankAccount(10)
        app.get_transaction_history(self.a)
        self.assertEquals(sys.stdout.getvalue(),'No transactions found\n')

    def test_get_transaction_history(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        self.a=app.BankAccount(10)
        self.a.withdraw(2)
        self.a.withdraw(5)
        beginning="ID   Timestamp    user Id  initial amount  final amount    difference\n"
        content=beginning+""
        for i, val in enumerate(self.a.transactions):
            content=content+str(i+1)+"   "+str(self.a.transactions[i])+"\n"
        app.get_transaction_history(self.a)
        self.assertEquals(sys.stdout.getvalue(),content)
        
        
if __name__ == '__main__':
    unittest.main()
