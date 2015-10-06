"""
    Usage: python <this-script-name>

"""

from subprocess import call
import re
import os


def download(code, start, end, fn):
    """download history data of a given stock from a given start data to a
    given end data, and then save the downloaded data into the given file.
    this function return 0 if success.
    e.g. cn_601318
    e.g. 20060101
    e.g. 20150831
    e.g. history.txt
    """

    return call(['phantomjs', 'download.js', code, start, end, fn])


def handle_downloaded_data(code, start, end, download_file, csv_file):
    """first, downloading history data of a given stock from a given start data
    to a given end data, and then save the downloaded data into the given file.
    then, processing the downloaded file, re-formatting it, creating a csv
    format file.
    e.g. cn_601318
    e.g. 20060101
    e.g. 20150831
    e.g. history.txt
    e.g. history.csv
    """

    assert download(code, start, end, download_file) == 0, 'failed to \
download history data.'

    with open(download_file) as f:
        msg = f.read()
    os.remove(download_file)

    splits = re.split('\[|\]', msg)

    with open(csv_file, 'w+') as fo:
        for each in reversed(splits):
            # otherwise `each` is something like `,`
            if len(each) > 50:
                each = each.replace('\"', '')
                each = each.replace(',', ', ')
                fo.write(each + '\n')
