import os
import re
from src.log import Log
from argparse import ArgumentParser
from config import HOST_IP, HOST_USERNAME, HOST_PASSWORD


parser = ArgumentParser()
parser.add_argument('-l', '--log_level', type=str, default='WARNING', help='設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING')
parser.add_argument('-H', '--host', type=str, default=None, help='指定連線主機，格式為ip:port')
parser.add_argument('-u', '--username', type=str, default=None, help='指定ssh連線使用者')
parser.add_argument('-p', '--password', type=str, default=None, help='指定ssh連線密碼')
parser.add_argument('-s', '--source_dir', type=str, default=None, help='指定來源資料夾')
parser.add_argument('-d', '--dest_dir', type=str, default=None, help='指定目的地資料夾')
parser.add_argument('-t', '--test', type=bool, default=False, help='是否為測試')
argv = parser.parse_args()

logger = Log(__name__)
logger.set_file_handler(file_amount=1)
logger.set_msg_handler()
logger.set_level(argv.log_level)

try:
    if HOST_IP:
        host = HOST_IP
    else:
        host = argv.host

    if HOST_USERNAME:
        username = HOST_USERNAME
    else:
        username = argv.username

    if HOST_PASSWORD:
        password = HOST_PASSWORD
    else:
        password = argv.password

    source_dir = argv.source_dir
    dest_dir = argv.dest_dir
except Exception as err:
    logger.error(msg=err, exc_info=True)

files = os.listdir(source_dir)
logger.debug(files)
max_number = 0
for file in files:
    m = re.search(r'(?P<num>\d{1,4})', file)
    if m:
        max_number = max(max_number, int(m.group('num')))
logger.debug(f'max_number: {max_number}')

for file in files:
    m = re.search(r'(?P<num>\d{1,4})', file)
    if m and int(m.group('num')) == max_number:
        command = f'sshpass -p {password} scp {username}@{host}:{dest_dir} {source_dir}/{file}'
        if not argv.test:
            os.system(command)
