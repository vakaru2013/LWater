from download import handle_downloaded_data

if __name__ == '__main__':
    """
    download history data of 601318, zhong guo ping an.
    """

    handle_downloaded_data('cn_600674', '20060101', '20150930', 'tmp.txt',
                           '2006-20150930-600674.csv')
