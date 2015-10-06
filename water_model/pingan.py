from fv2 import BonusShare, prepare_history, print_ror


if __name__ == '__main__':
    bonusinfo = BonusShare('data/601318/bonusshare.csv')
    csv = prepare_history('data/601318/03022007-09302015.csv',
                          'data/601318/03022007-09302015-10daysperline.csv',
                          10)
    bgdate = '2007-03-08'
    enddate = '2015-09-23'
    print_ror(bonusinfo, csv, bgdate, enddate)
