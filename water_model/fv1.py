"""
Feature vector 1.

short target:
    get an rdd of feature vector for every day in the raw csv,

    >>>>>>>this is called rdd1

    see how many different fvs the rdd contains

    >>>>>>this number value can be obtained from rdd1 using rdd api

    so, done!

short target 2:
    see each different fv appears how many times
    print:
	0, ------------------
	1,fv value, not 1-of-k encode (means decode from 1-of-k)
	2,repeated times
	3,repeated date 1,
	    repeat data 2,
	    ...
	4,done, then should follow next fv value
	5,-------------------

    
    >>>>>>>>> first, see how word count app is done in spark.


the feature vector:
    123456789
	    ^
	 ^^^
    so, f1: compare 9 to min and max of 678, select the max-diff value, (signed)max-diff/max-or-min-678, 
					when the diff are same, using the latest day as max-or-min-678.
		1-of-k, k is 5, -0.2~0.2:   00001
				-0.4~-0.2:  00010
				?~-0.4:	    00100
				0.2~0.6:    01000
				0.6~?:	    10000

		     when decode, it is 1,2,3,4,5 accordingly.

    123456789
	 ^
      ^^^

    so, f2: the same as above

    123456789
	  ^^^
    ^^^^^^

    so, f3: compare the mean of 789 to the mean of 1-6,
		using the same encoding way as above


1,open raw csv using spark and generate rdd from it
2,
"""

from format import format

def prepare():
    format('data/03022007-07242015.csv', 'data/fv1_raw.csv', 14)


if __name__ == '__main__':
    prepare()

