'''
this script test `output` module
'''

from output import output
from output import return_rate

pre = output('train_data.csv')
print pre
rate = return_rate(pre)

