"""
    Usage: python <this-script-name>

"""

from subprocess import call
import mail.helper
import re
import time
import os

msgfile='emailMsg'

pingan='sh601318'
chuantou='sh600674'

originAPrice='32.6'
originBPrice='11.42'

stockA=pingan
stockB=chuantou


while True:
    code=call(['phantomjs', 'compare.js', '1.02', msgfile, stockA, originAPrice, stockB, originBPrice]);

    if(code == 1):
	# read the file
	with open(msgfile) as file:
	    msg=file.read()
	# send email
	plain_text_email = mail.helper.plain(
	    msg,
	    from_name = 'robot',
	    from_email = 'xx@xx.com',
	    to='xx@xx.com',
	    subject='Stock Selling and Buying Now!',
	 )

	mail.helper.send_smtp(
	    plain_text_email,
	    verbose=False,
	    host='smtp.xx.com', # smtp server
	    username='xx@xx.com',
	    password='xx',
	    starttls=False,
	)

	# update original prices
	splitmsg=re.split('\n',msg)
	splitmsg=re.split(': |, ',splitmsg[1]) 
	originBPrice=splitmsg[1]
	originAPrice=splitmsg[3]
	stockA,stockB=stockB,stockA
	os.remove(msgfile)	
    # sleep 60 seconds
    time.sleep(60);
