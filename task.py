class BankAccount:
   def __init__(self, account_no, balance, owner_name, open_date):
      self.account_no = account_no
      self.balance = balance
      self.owner_name = owner_name
      self.open_date = open_date
      self.is_closed = False  # Added to track closure state

   def deposit(self, value):
      if self.is_closed:
         print(" Account is closed. Cannot deposit.")
         return
      self.balance += value 
      print(f"{self.owner_name} deposited {value}")

   def check_balance(self):
    
      if self.is_closed:
         print("Account is closed.")
         return
      print(f"Your balance is {self.balance}")

   def withdraw(self, amount):
      if self.is_closed:
         print("Account is closed. Cannot withdraw.")
         return
      
      if self.balance >= amount:
         self.balance -= amount 
         response = "Your withdrawal was successful"
      else:
         response = "Balance is insufficient"
      print(response)
      return response
      
   def display_info(self):
      print("User details")
      print(f"Account_no: {self.account_no}, Balance: {self.balance}, Name: {self.owner_name}, Open_date: {self.open_date}")
      print("_______________________________")
      
   def close_account(self):
      if self.is_closed:
         print("Account is already closed.")
         return
      self.is_closed = True
      self.balance = 0
      print("Account closed successfully.")


customer1 = BankAccount(556655, 10000, 'Frank', "12/6/2026")

customer1.deposit(20000)
customer1.withdraw(10000)
customer1.check_balance()
customer1.display_info()
customer1.close_account()
customer1.display_info() 