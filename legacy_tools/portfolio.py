"""
    Usage: python <this-script-name>

    Modify `codes` object to add or remove stock from your portfolio.
    Currently this script can support China ShangHai stocks and HongKong stocks.
    Code format:
	`sh601318` if the stock belongs to ShangHai and its numerial code is 601318
	`rt_hk21478` if the stock belongs to Hongkong and its numerial code is 21478 
 
"""

from subprocess import call
import mail.helper
import re
import time
import os

codes=['rt_hk01918','rt_hk21478','rt_hk00656','rt_hk03333','sh601318']

while True:
    for code in codes:
        call(['phantomjs', 'printprice.js', code]);
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    # sleep 60 seconds
    time.sleep(60);
