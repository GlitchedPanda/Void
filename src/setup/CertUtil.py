import os
import subprocess
from pathlib import Path

from util.Logger import logger

def is_cert_installed():
	error_code = subprocess.call(f'certutil -store -user Root mitmproxy', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	logger.info(f"Certificate is {'not ' if error_code else ''}installed")
	return not bool(error_code)
    	

def install_cert():
	logger.warning('Installing mitmproxy certificate...')


	crtPath = Path.home() / '.mitmproxy' / 'mitmproxy-ca-cert.cer'
	logger.debug(f'certificate path: "{crtPath}"')

	if error_code := subprocess.call(f'certutil -addstore -user Root "{crtPath}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
		logger.error(f'Certificate could not be installed: {hex(error_code)} - {str(error_code).strip()}')
		os._exit(1)
	else:
		logger.info('Certificate was successfully installed') 

def delete_cert():
	logger.warning('Deleting mitmproxy certificate...')

	if error_code := subprocess.call(f'certutil -delstore -user Root mitmproxy', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
		logger.error(f'Certificate could not be deleted: {hex(error_code)} - {str(error_code).strip()}')
		os._exit(1)
	else:
		logger.info('Certificate was successfully deleted') 		   