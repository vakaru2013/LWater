"""
Feature vector model No.2

short target:

    calculate the rate of stock return, if it is good, I am a genius.

    a list, each item in it is a dict, its key is a feature vector, while its
    value is all lineidx whose fv equal to the key.

    then, a function, print info into a file like this:

        fv: [......]
        date:
            date1,
            date2,
            ...

        -------

        then repeat to print info of another fv

        -------

    then, a function, given a date info, return a list of date info whose fv
    equal to the given date.

the feature vector:
    1234567890  -- the latter 5 are used for outcome/label
       ^
        ^  --
      ^
       ^   --   trend combination
    ^^^
       ^^  -- mean variation
"""

from format import format


class CSV:
    def __init__(self, fp, itemsperday=10):
        """given file path of the csv, this csv file containing history
        informaiton of a stock, each line contains multiple days' info.
        """

        self.inited = False

        with open(fp) as f:
            l = f.readline()
            items = l.split(', ')
            # each line contains multiple day's info.
            self.daysperline = len(items) / itemsperday

        self.fp = fp
        self.itemsperday = itemsperday

        # each item in it is a list, the list contains all items of a line
        self.lineitems = []
        with open(fp) as f:
            for l in f:
                self.lineitems.append(l.split(', '))

        # each item in it is a feature vector of a line
        self.fvs = []
        for i in range(len(self.lineitems)):
            self.fvs.append(self.fv(line=i))

        self.inited = True

    def vol(self, lineidx, dayidx):
        """return volume value of in the line by index and the day by index --
        start from 0.
        because each line contains multiple day's info.
        """

        return float(self.lineitems[lineidx][8 + self.itemsperday * dayidx])

    def ratiorank(self, ratio):
        """given a ratio, return a rank value.
        the rank value is from 0~6,
        the higher value means the ratio is larger.
        """

        rank = {
            0.5: 0,
            0.75: 1,
            0.85: 2,
            1.1: 3,
            1.25: 4,
            1.7: 5
        }
        for key, val in rank.iteritems():
            if ratio < key:
                return val
        return 6

    def f1(self, **kwargs):
        """return the first feature of a date in the csv file,
        either date=2015-06-25, or line=0.
        the return value is a ratio rank value.
        """

        if 'line' in kwargs:
            lineidx = kwargs['line']
        elif 'date' in kwargs:
            lineidx = self.linebydate(kwargs['date'])

        if self.inited is True:
            return self.fvs[lineidx][0]

        mean1 = (self.vol(lineidx, 0) + self.vol(lineidx, 1) +
                 self.vol(lineidx, 2)) / 3
        mean2 = (self.vol(lineidx, 3) + self.vol(lineidx, 4)) / 2

        ratio = mean2 / mean1
        return self.ratiorank(ratio)

    def f23(self, **kwargs):
        """return the 2nd and 3rd features of a date in the csv file,
        either date=2015-06-25 or line=0.
        the return value is a list containing two rank values.
        """

        if 'line' in kwargs:
            lineidx = kwargs['line']
        elif 'date' in kwargs:
            lineidx = self.linebydate(kwargs['date'])

        if self.inited is True:
            return self.fvs[lineidx][1:]

        vol3 = self.vol(lineidx, 2)
        vol4 = self.vol(lineidx, 3)
        vol5 = self.vol(lineidx, 4)

        rt54 = vol5 / vol4
        rt43 = vol4 / vol3
        return [self.ratiorank(rt43), self.ratiorank(rt54)]

    def fv(self, **kwargs):
        """return a feature vector of a date in the csv file,
        either date=2015-06-25 -- calculate and reuturn that day's feature
        vector, or line=0 -- calculate and return the feature vector of that
        line.
        """

        if 'line' in kwargs:
            lineidx = kwargs['line']
        elif 'date' in kwargs:
            lineidx = self.linebydate(kwargs['date'])

        return [self.f1(line=lineidx)] + self.f23(line=lineidx)

    def linebydate(self, date):
        """given a date, return line idx of that date,
        although every line contains multiple days' info,
        here the date is the major day.

        date format: 2015-06-25
        """

        assert date >= self.majordate(0) and \
            date <= self.majordate(len(self.lineitems) - 1), \
            'date %s is out of scope of the csv %s, (%s, %s)' % \
            (date, self.fp, self.majordate(0),
             self.majordate(len(self.lineitems) - 1))

        for i in range(len(self.lineitems)):
            if date == self.majordate(i):
                return i
        raise Exception('can\'t find lineidx in csv for: ' + date)

    def date(self, lineidx, dayidx):
        """given lineidx and dayidx, return the date,
        both indexes start from 0.

        date formate is: 2015-06-25
        """

        return self.lineitems[lineidx][self.itemsperday * dayidx]

    def majordate(self, lineidx):
        """given a lineidx, return its major date,
        major date is something like the current day,
        as one line contains multiple days' info,
        but there is something like current day.
        """

        return self.date(lineidx, 4)

    def closeprice(self, **kwargs):
        """given a date, return its closing price,
        e.g.
        date='2015-06-25'
        or, given the lineidx and the dayidx
        e.g.
        lineidx=0
        dayidx=4
        """

        if 'date' in kwargs:
            lineidx = self.linebydate(kwargs['date'])
            dayidx = 4

        return float(self.lineitems[lineidx][self.itemsperday * dayidx + 2])

    def predict(self, date):
        """ given a date, return prediction -- price will up, down or
        unchanged. the date's format: 2015-06-25
        """

        fv = self.fv(date=date)
        f1 = fv[0]
        f2 = fv[1]
        f3 = fv[2]

        if f2 >= 5 or f3 >= 5 or f1 >= 5:
            return 'up'
        elif f2 <= 1 or f3 <= 1 or f1 <= 1:
            return 'down'
        else:
            return 'flat'

    def predictbyline(self, lineidx):
        """ given lineidx, return prediction
        """

        return self.predict(self.majordate(lineidx))


class ROR:
    """
    calculate the rate of stock return, if it is good, I am a genius.

    given a begin date, an end date (however, no deal will be made in the end
    day -- neither buy nor sell),
    and given the initial state -- hold cash or hold stock,

    if it is holding stock, then the closing price of that begining day is used
    as reference,
    from a relative long run, whether using closing price or opening price will
    generally lead no big difference, for convenience, the closing price of the
    begining date is used.

    assuming the initial cash is 100 unit (if holding cash), or initial stock is
    100 shares (if holding stock).

    implementation:
    1, calculate the initial money, 100 unit(if holding cash) or closing price*
    100 shares(if holding stock).
    2, every time when an event happened, update and remember the new state --
    holding cash or holding stock shares. And:
        1, if it is a selling event, then calculate and remember the money:
            using selling price * stock shares number
        2, otherwise, calculate and remember the shares of stock,
        using cash/buying price
    3, at the end, calculate (if need) and return the final money:
        using shares of stock* closing price of that day (if holding stock).
    """

    def __init__(self, bgdate, enddate, initcash, csv, bonusshares):
        """given a begin date, an end date, and the initial state --
        hold cash or hold stock: True or False.
        and given a csvobj, which represents history info of stock.
        and given a BonusShares object, containing bonus share issuing info.
        bgdate and enddate's format: 2015-06-25
        """

        self.bonusshares = bonusshares

        self.bgdate = bgdate
        self.enddate = enddate
        # initial state whether is holding cash
        self.initcash = initcash
        self.csv = csv

        self.initmoney = 100 if initcash is True else \
            100 * csv.closeprice(date=bgdate)

        # latest state whether is holding cash
        self.bcash = initcash
        # latest cash, valid only when state is holding cash,
        # otherwise, ignore it
        self.cash = 100.0
        # latest shares, valid only when state is holding share,
        # otherwise, ignore it
        self.shares = 100.0

        # key is date, value is 'buy', 'sell' or 'stay'
        self.decisions = {}

    def ror(self, bbuyandhold=False):
        """return rate of return.
        1, iterate from the bgdate to enddate, using lineidx in the csv file,
        get prediction, and get decision,

        2, given decision of a day, know the action: convert cash to stock,
        or convert stock to cash, or stay unchanged, calculate and remember the
        latest state, number of shares and cash unit.

        3, after the last day is processed, we get the final state.

        4, then, convert to money, and compare to the initial money, and get the
        rate of return.

        there is a special parameter, bbuyandhold, when it is True then no sell.
        this can be used for compareing purpose.
        """

        for i in range(self.csv.linebydate(self.bgdate),
                       self.csv.linebydate(self.enddate)):
            mjdate = self.csv.majordate(i)
            self.handle_bonusshare(mjdate)
            if bbuyandhold is False:
                pred = self.csv.predictbyline(i)
                dec = self.decision(self.bcash, pred)
                dp = self.csv.closeprice(date=mjdate)
                self.deal(dec, dp, mjdate)

        return self.money(self.enddate) / self.initmoney

    def handle_bonusshare(self, date):
        """given date, check if there is any bonus shares,
        if yes, then handle it:
        if current state is holding stock shares, then modify the shares
        accroding to the bonus share issuing info.
        if current state is holding cash, then do nothing.
        """

        bonus = self.bonusshares.check(date)
        if bonus is not None:
            if self.bcash is False:
                old = self.shares
                self.shares = self.shares / bonus[0] * bonus[1]
                print 'shares holded was %0.2f, now becomes %0.2f, %s...' % \
                    (old, self.shares, date)

    def decision(self, bcash, pred):
        """ given current state -- holding cash or holding stock,
        and given prediction -- price will up, down or unchanged,
        return decision -- buy, sell or stay unchanged.
        """
        if bcash is True:
            if pred == 'up':
                return 'buy'
            else:
                return 'stay'

        else:
            if pred == 'down':
                return 'sell'
            else:
                return 'stay'

    def deal(self, dec, dp, date):
        """
        given decision, given the deal price, and date,
        update the latest status -- holding cash or stock,
        and update the money -- cash unit or stock shares.
        this function will also store all decision info in this instance.
        """
        if dec == 'stay':
            pass
        elif dec == 'buy':
            assert self.bcash is True, 'can\'t buy when holding stock shares.'
            self.shares = self.cash / dp
            self.bcash = False
            print 'buying, %s, %0.2f' % (date, dp)
        elif dec == 'sell':
            assert self.bcash is False, 'can\' sell when holding cash.'
            self.cash = self.shares * dp
            self.bcash = True
            print 'selling, %s, %0.2f' % (date, dp)
        else:
            raise Exception('invalid deal decision.')

    def money(self, date=None):
        """return money number, date may be needed as input, because if it is
        holding shares, need date to calculate the latest price.
        """

        if self.bcash is True:
            return self.cash

        assert date is not None, 'must specify date in order to calculate \
            money when holding stock shares.'

        return self.shares * self.csv.closeprice(date=date)


def prepare_history(incsv, outcsv, daysperline):
    """given a input csv filename, which is a raw history csv file, each line
    contains only one day's info,
    and given daysperline, then this function generates a
    new csv file, each line contains multiple days info,
    finally this function returns a CSV object based on that new csv file.
    """

    format(incsv, outcsv, daysperline)
    return CSV(outcsv)


class BonusShare:
    """this class contains information about the bonus share issue info.
    """

    def __init__(self, bonus_file):
        """given a bonusshare file, which is a csv file.
        """

        # this is a dictionary, the key is date, e.g. '2015-06-25',
        # the value is a list, e.g. [10, 20], means issuing 10 new shares for
        # every 10 old shares.
        self.bonusinfo = {}

        with open(bonus_file) as f:
            for l in f:
                l = l.rstrip('\n')
                items = l.split(', ')
                self.bonusinfo[items[0]] = [float(i) for i in items[-2:]]

    def check(self, date):
        """given date, return None or a list, e.g. [10, 20],
        means issuing 10 new shares for
        every 10 old shares.
        """

        return self.bonusinfo.get(date, None)


def print_ror(bonusinfo, csv, bgdate, enddate):
    """
    this is an entry function.
    """

    ror = ROR(bgdate, enddate, True, csv, bonusinfo)

    print 'rate of return: %0.2f, ending date: %s, ending close price: %0.2f' \
        % (ror.ror(), enddate, csv.closeprice(date=enddate))

    ror = ROR(bgdate, enddate, False, csv, bonusinfo)
    print 'rate of return if buy and hold: %0.2f' % ror.ror(True)
    print 'begin date: %s' % bgdate
