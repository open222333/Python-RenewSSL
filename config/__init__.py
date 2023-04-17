from configparser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')


HOST_IP = conf.get('TRANSFER', 'HOST_IP', fallback=None)
HOST_USERNAME = conf.get('TRANSFER', 'HOST_USERNAME', fallback=None)
HOST_PASSWORD = conf.get('TRANSFER', 'HOST_PASSWORD', fallback=None)
