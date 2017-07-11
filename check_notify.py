#!/usr/bin/env python
import config
import smtplib
import time
import urllib2

from bs4 import BeautifulSoup

# Coinmarket Cap ETH
search_url = 'https://coinmarketcap.com/currencies/ethereum/'
content = urllib2.urlopen(search_url).read()
soup = BeautifulSoup(content, "lxml")

run = True

#returns price as float
def parse_price():
    str_price = soup.find(id = 'quote_price').getText()
    ascii_price = (str_price.encode('ascii'))
    price = float(ascii_price[1:])
    return price

def compare_price(value):
    if value <= config.lower_limit or value >= config.upper_limit:
        return True
		
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
    
    while run:
        price = parse_price()
        try:
            if compare_price(price):
                send_email(config.email_address, config.password)
                time.sleep(1800) #code only runs once every half an hour

        except:
            print("Error. Program exiting")
            run = False