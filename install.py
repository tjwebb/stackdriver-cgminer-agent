import os
import sys
import subprocess
import paramiko
import random
from pathlib import Path
from urllib.request import urlretrieve

GOPATH = os.environ['GOPATH']
cacert_url = 'https://curl.haxx.se/ca/cacert.pem'
cacert_file = '/tmp/cacert.pem'
oauth2l_bin = f'{GOPATH}/bin/oauth2l'
gcp_credentials_file = '/tmp/gcp_credentials.json'

def show_help():
    print('Usage: \n\tpython install.py <miner_ip> <ssh user> <ssh password>')
    print('\nExample: \n\tpython install.py 192.168.1.150 root admin\n')
    sys.exit()


if len(sys.argv) == 1 or sys.argv[1] == 'help':
    show_help()

# validate cli args
if len(sys.argv) < 2:
    print('Error: miner_ip is required')
    show_help()

if len(sys.argv) < 3:
    print('Error: ssh user is required')
    show_help()

if len(sys.argv) < 4:
    print('Error: ssh password is required')
    show_help()

# download latest CA Cert for curl
if Path(cacert_file).is_file():
    print('CA cert file: exists.')
else:
    print('Downloading curl CA cert...')
    urlretrieve(cacert_url, cacert_file)

# download and install oauth2l
if Path(oauth2l_bin).is_file():
    print('oauth2l: exists')
else:
    print('Installing oauth2l tool...')
    subprocess.run(['go', 'get', '-u', 'github.com/google/oauth2l'])
    subprocess.run(['go', 'install', 'github.com/google/oauth2l'])

# create service account
print('Creating GCP service account...')

# get current project
cur_project = subprocess.run([
    'gcloud', 'config', 'list',
    '--format', 'value(core.project)'
], capture_output=True).stdout.decode()

#service_acct_name = f'miner-logwriter@{cur_project}.iam.gserviceaccount.com'
service_acct_salt = random.randint(10, 1000)
service_acct_name = f'miner-logwriter-{service_acct_salt}'

# create service account key
print('Generating service account token...')
# check if service account exists...
# gcloud iam service-accounts list --format 'value(email)' --filter='email ~ ^ miner-logwriter@'
service_acct_exists = subprocess.run([
    'gcloud', 'iam', 'service-accounts', 'list',
    '--format', '\'value(email)\'', '--filter=\'email ~ ^ miner-logwriter@\''
], capture_output=True).stdout.decode()

if service_acct_exists is None:
    subprocess.run([
        'gcloud', 'iam', 'service-accounts', 'create', 'miner-logwriter', #service_acct_name,
        '--description', 'Service account for miners writing logs to Stackdriver'
    ], check=True)

# generate token
# TODO generate in python instead
oauth2l_proc = subprocess.run([
    f'{GOPATH}/bin/oauth2l',
    'header',
    '--credentials',
    gcp_credentials_file,
    '--scope',
    'cloud-platform'
], capture_output=True)

token_header = oauth2l_proc.stdout.decode()


# TODO
#client = paramiko.SSHClient()
#client.connect(
