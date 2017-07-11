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
    evaluate = False
    if value <= config.lower_limit or value >= config.upper_limit:
        evaluate = True
    return evaluate

#sends email from email in config file to same email
def send_email(address, password, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(address, password)
    
    msg = "The price of ETH is outside your limit $" + str(price) + "."
    server.sendmail(address, address, msg)
    server.quit()

if __name__ == '__main__':
    
    while run:
        try:
            current_price = parse_price()
            if compare_price(current_price):
                send_email(config.email_address, config.password, current_price)
                print "Log: email sent"
                time.sleep(3600) #code only runs once every half an hour

        except:
            print("Error. Program exiting")
            run = False