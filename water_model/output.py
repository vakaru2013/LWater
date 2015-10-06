import re

'''
this function calculates and returns a list of predictions for every day,
each item in the list contains date, closing price, and prediction.


each prediction output is an int value:
    2 is `will up`, 
    1 is `remain unchanged`, 
    0 is `will down`


parameters:
    raw_csv: 
    a string indicating the file path of a raw dataset like trainset.csv or testset.csv downloaded from sohu.com

    feature_cnt:
    using prices of the consecutive specified number of days as machine learning features 

    predict_scope:
    predicting price trend in the following specified number of days
    
    threshold:
    the price will go up or down or remain unchanged.
    when price variance is within 1%, we say the output is `remain unchanged`
'''
def output(raw_csv, feature_cnt=20, predict_scope=5, threshold=0.01):
    # array of dictionary for every day
    # each dict contains date, closing price, and prediction
    predicts=[]
    with open(raw_csv) as fi:
	for line in fi:
	    item = { 
		'date' : re.split(', ', line)[0],
		'close_price' : float( re.split(', ', line)[2] ),
	    }
	    predicts.append( item )
    
    # calc the max and min closing prices in the following specified number of days 
    for idx, val in enumerate( predicts[feature_cnt-1:][:-predict_scope] ):
	cur=val['close_price']
	follows=[ i['close_price'] for i in predicts[ feature_cnt + idx : feature_cnt + idx + predict_scope ] ]
	
	if min(follows) >= cur:
	    if max(follows) / cur > 1 + threshold:
		predict = 2
	    else:
		predict = 1
	elif max(follows) <= cur:
	    if min(follows) / cur < 1 - threshold:
		predict = 0
	    else:
		predict = 1
	else:
	    if cur - min(follows) >= max(follows) - cur:
		if min(follows) / cur < 1 - threshold:
		    predict = 0
		else:
		    predict = 1
	    else:
		if max(follows) / cur > 1 + threshold:
		    predict = 2
		else:
		    predict = 1

	predicts[feature_cnt-1:][:-predict_scope][idx]['predict'] = predict

    # return valid part
    return predicts[feature_cnt-1:][:-predict_scope]


'''
this function return rate of return based on predictions.
it assumes we hold cash at the begining, 
then buy when prediction is `up`,
and sell when prediction is `down`.


parameters:
    predicts
    a list of predictions, containing date, closing price, and prediction.
'''
def return_rate(predicts):
    cash = True
    pbuy = 0
    rate = 1
    for i in predicts:
	if i['predict'] == 2:
	    if cash == True:	    
		pbuy = i['close_price']
		cash = False
		print 'bought at: ' + str(pbuy) + ' when: ' + i['date']
	elif i['predict'] == 0:
	    if cash == False:
		psell = i['close_price']		
		rate = rate * psell / pbuy
		cash = True
		print 'sold at: ' + str(psell) + ' when: ' + i['date']
		print 'single rate of return: ' + str(psell/pbuy) + '\n'
    print 'total rate of return: ' + str(rate)    
    return rate 

