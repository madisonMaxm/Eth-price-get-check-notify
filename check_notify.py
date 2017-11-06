#!/usr/bin/env python
import config
import smtplib
import time
import urllib2
import sys
import traceback

from bs4 import BeautifulSoup

# Coinmarket Cap ETH
search_url = 'https://coinmarketcap.com/currencies/ethereum/'

run = True

#returns price as float
def parse_price():
    content = urllib2.urlopen(search_url).read()
    soup = BeautifulSoup(content, "lxml")

    #convert text from unicode to float with 2 degrees of precision
    str_price = soup.find(id = 'quote_price').getText()
    price = int(float(str_price[1:].encode('utf-8'))*100)/100.0
    
    #print type(price)
    print "Log: $%.2f" % (price)
    
    soup.decompose()
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

                print "email sent"
        
            time.sleep(60) #code only runs once every half an hour

        except:
            print("Error. Script aborted.")
            traceback.print_exc()
            run = False