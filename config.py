class Currency(object):
    
    def __init__(self, name, low, high):
   
        self.name = name
        self.low = low
        self.high = high
#enter any new coinmarket cap listed currency in the following format: Currency(name of currency, low limit (integer), high limit (integer))
ethereum = Currency('ethereum', 280, 290)
neo = Currency('neo', 18, 20)

currency_array = []

currency_array.append(ethereum)
currency_array.append(neo)

#program sleep duration. units = seconds
time_inverval = 1800

#must be gmail email address. If you use two step authentification, you will need to use an app password: https://support.google.com/accounts/answer/185833
email_address = ''
password = '' 
