from fv2 import BonusShare, prepare_history, print_ror


if __name__ == '__main__':
    bonusinfo = BonusShare('data/600674/bonusshare.csv')
    csv = prepare_history('data/600674/2006-20150930-600674.csv',
                          'data/600674/2006-20150930-600674-10daysperline.csv',
                          10)
    bgdate = '2006-01-10'
    enddate = '2015-09-23'
    print_ror(bonusinfo, csv, bgdate, enddate)
