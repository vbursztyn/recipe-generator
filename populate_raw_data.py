import os


import requests


import zipfile


from config import get_config


if __name__ == '__main__':
	config = get_config()

	request = requests.get(config['DOWNLOAD_USDA'])

	usda_zip_path = os.path.join(config['RAW_DATA'], config['USDA_ZIP'])

	with open(usda_zip_path, 'wb') as f_zip:
	    f_zip.write(request.content)

	zip_extract = zipfile.ZipFile(usda_zip_path, 'r')
	zip_extract.extractall(config['RAW_DATA'])
	zip_extract.close()