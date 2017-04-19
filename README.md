# Test assignment for the QA engineer position
## Application
The system under test is a simple command line application. It consists of two classes `BankAccount` and `Transaction`. 
The user is prompted to create a bank account by specifying amount of available funds. After the account is created user can choose between three options: add funds to the account, withdraw founds from the account or list account's transactions. Transaction object is created every time when user perform an action with the BankAccount object (add or withdraw funds). Transaction object has following fields: timestamp, ip address of a user, initial and final amound of funds and the difference. User's IP is obtained with the third-party service call over http. 
## Instructions
The app consists of 2 files: `app.py` and `test.py`. The app is compatible with `python2.7`. Install module `requests` using `pip install requests`. In order to run the app and tests execute following command in the terminal:
For Linux:
```
python app.py
python test.py
```
For Windows:
```
app.py
test.py
```
## Assignment
Fork this repository. Clone forked repo to your local machine.
The task is to cover with unit tests both classes - `BankAccount` and `Transaction`. Write your tests in `test.py` file. Try to achive reasonable coverage (~90%). Third-party service call should be mocked out.
Push your changes back to forked repository.
