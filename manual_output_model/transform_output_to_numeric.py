with open('volume_predict.csv') as fi:
    with open('volume_predict_number.csv', 'w+') as fo:
	content=fi.read()
	content=content.replace('will up', '2000000')
	content=content.replace('will down', '0')
	content=content.replace('can\'t', '1000000')
	fo.write(content)



