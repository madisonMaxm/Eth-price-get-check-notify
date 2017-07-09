#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import smtplib
import config

# Coinmarket Cap ETH
search_url = 'https://coinmarketcap.com/currencies/ethereum/'
content = urllib2.urlopen(search_url).read()
soup = BeautifulSoup(content, "lxml")

str_price = soup.find(id = 'quote_price').getText()
ascii_price = (str_price.encode('ascii'))
price = float(ascii_price[1:])

def compare_price():
	if price <= config.lower_limit or price >= config.upper_limit:
		return true
		
#sends email from email in config file to same email
def send_email(address, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(address, password)
    
    msg = "The price of ETH is outside your limit $" + str(price) + "."
    server.sendmail(address, address, msg)
    server.quit()
   
if __name__ == '__main__':
    try:
       parse_price()
      
       send_email(config.email_address, config.password)

    except:
		pass