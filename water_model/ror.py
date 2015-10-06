import sys
from fv2 import BonusShare, prepare_history, print_ror


if __name__ == '__main__':
    """
    example:
        python ror.py 000651
    example 2:
        python ror.py 000651 2006-01-11 2015-09-23
    """

    code = sys.argv[1]
    try:
        start = sys.argv[2]
    except:
        start = '2006-01-11'
    try:
        end = sys.argv[3]
    except:
        end = '2015-09-23'

    bonus = 'data/%s/bonusshare.csv' % code
    bonusinfo = BonusShare(bonus)
    csv = prepare_history(
        'data/%s/20060101-20150930-cn_%s.csv' % (code, code),
        'data/%s/20060101-20150930-cn_%s-10daysperline.csv' % (code, code),
        10)
    print_ror(bonusinfo, csv, start, end)
