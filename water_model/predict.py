import re

from pyspark import SparkConf, SparkContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import LinearRegressionWithSGD
from output import output
from output import return_rate

"""
this function returns a list of volumes for every day

parameters:
    raw_csv:
    a string indicating the file path of a trainset.csv downloaded from sohu.com
"""

def volumes(raw_csv):
    with open(raw_csv) as fi:
	return [ float( re.split( ', ', line )[8] ) for line in fi ]


feature_cnt = 20 # using prices of the consecutive specified number of days as machine learning features
predict_scope = 5 # predicting price trend in the following specified number of days

volume_list = volumes('trainset.csv')

input_list = []
for idx, val in enumerate(volume_list[feature_cnt-1:][:-predict_scope]):
    features = volume_list[idx:][:feature_cnt]
    input_list.append([ each/features[0] for each in features ])

output_list = output('trainset.csv', feature_cnt = feature_cnt, predict_scope = predict_scope)

inputlen = len(input_list)
outputlen = len(output_list)
print 'count of input in train dataset:', inputlen
print 'count of output in train dataset:', outputlen

print input_list
print [ output_list[idx]['predict'] for idx in range(outputlen) ]


assert inputlen == outputlen, 'something wrong, can\'t continue...'

points = [ LabeledPoint( output_list[idx]['predict'], input_list[idx] ) for idx in range( outputlen ) ]

if __name__ == '__main__':
    conf = SparkConf().setMaster("local").setAppName("StockPred")
    sc = SparkContext(conf = conf)
    points = sc.parallelize(points)
    points.cache()
    model = LinearRegressionWithSGD.train( points, iterations=200, intercept=True )
    print "Final weights: " , model.weights
    print "Final intercept: " , model.intercept

    sc.stop()



