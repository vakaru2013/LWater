import sys
from download import handle_downloaded_data

if __name__ == '__main__':
    """
    download history data of a given stock.

    the first argument is the stock code, e.g. 601318, which is
    Zhong Guo Ping An.

    the second and third arguments are starting date and ending date, there are
    default values if no argument is provided.

    the downloaded info is stored in a csv file, the file name contains the
    stock code.

    example 1 - using default date:
        python getany.py 601318
    example 2:
        python getany.py 20060101 20150930
    """

    code = 'cn_' + sys.argv[1]
    try:
        start = sys.argv[2]
    except:
        start = '20060101'
    try:
        end = sys.argv[3]
    except:
        end = '20150930'
    fn = '%s-%s-%s.csv' % (start, end, code)
    handle_downloaded_data(code, start, end, 'tmp.txt', fn)
