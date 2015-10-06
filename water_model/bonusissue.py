"""
check whether there is bonus issue.
chinese: pai-song-gu-fen,
e.g. every 10 shares issue 10 more shares.
"""

import sys


def check(csvf):
    """given a csv file, print info if found there is bonus issue.
    """

    # previous close price
    pcp = 0
    with open(csvf) as f:
        for line in f:
            line = line.rstrip('\n')
            items = line.split(', ')
            # close price
            cp = float(items[2])
            # price rise percent or decline percent, it is a float value
            # e.g. 0.02
            rise = float(items[4][:-1])/100

            if pcp is 0:
                pass
            elif (cp - pcp) / pcp - rise < -0.05:
                # when run to here, means: today's close price is not normal
                # when compared with the previous day's close price, it is more
                # than 5 point percent lower than the rise percent given by the
                # declared rise percent. so it is very much likely to be a bonus
                # issue.
                print 'close price of %s: %0.2f, previous day\'s \
close price: %0.2f, the exception value: %0.3f...' % \
                    (items[0], cp, pcp, (cp - pcp) / pcp - rise)
            pcp = cp

if __name__ == '__main__':
    """given a raw csv file, each line contains one day's info.
    """

    check(sys.argv[1])
