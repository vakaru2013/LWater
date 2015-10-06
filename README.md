# LWater

Feature1:
---------------

Two stocks in my portfolio are ChuanTou (code: SH600674) and PingAn (code: SH601318). I have a very simple strategy to sell one and buy another according to their real time prices.

The chuantouPinganCompare.py keeps a js script running.

The js script uses phantomjs for getting real time prices of two of my stocks from a web service provided by SINA, once the script decides it is the time to sell one and buy another according to my dynamic strategy, it will notify the python script via writting information to a temp file.

Then the python script sends email to end user. 


Feature2:
---------------

portfolio.py can be used to print real time prices of all stocks in your portfolio.
