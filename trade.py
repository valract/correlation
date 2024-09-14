import subprocess
import sys

# List of libraries to check
libraries = [
    'requests',
    'pandas',
]

def install_package(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_and_install_libraries(libraries):
    """Check if libraries are installed and install them if not."""
    for library in libraries:
        try:
            __import__(library)
        except ImportError:
       	    if library == 'sklearn':
       	    	library = 'scikit-learn'
            install_package(library)

if __name__ == "__main__":
    check_and_install_libraries(libraries)


import requests
import pandas as pd

url = 'https://www.mataf.io/api/tools/csv/correl/snapshot/forex/50/correlation.csv?symbol=AUDCAD|AUDCHF|AUDJPY|AUDNZD|AUDUSD|CADCHF|CADJPY|CHFJPY|EURAUD|EURCAD|EURCHF|EURGBP|EURJPY|EURNZD|EURUSD|GBPAUD|GBPCAD|GBPCHF|GBPJPY|GBPNZD|GBPUSD|NZDCAD|NZDCHF|NZDJPY|NZDUSD|USDCAD|USDCHF|USDJPY'
filename = 'correlation.csv'

response = requests.get(url)
if response.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(response.content)
else:
    print(f'Failed to download file (status code: {response.status_code})')

with open(filename, 'r') as file:
    lines = file.readlines()

with open(filename, 'w') as file:
    file.writelines(lines[3:])

df = pd.read_csv(filename)
disp = {'5min':[], '15min':[], '1h':[], '4h':[], 'day':[], 'week':[]}
disn = {'5min':[], '15min':[], '1h':[], '4h':[], 'day':[], 'week':[]}

for index, row in df.iterrows():
    for column, value in row.items():
        try:
            if int(value) >= 80:
                disp[column].append([row[0], row[1], value])
            elif int(value) <= -80:
                disn[column].append([row[0], row[1], value])
        except ValueError: continue

print('\n************************************************************************\n\nNegative:')
for key, value in disn.items():
    print()
    print(key)
    for v in value:
        if v[0][3:] == v[1][:3]:
            print(f'{v[0][:3]}{v[1][3:]}', end=' ')
            print(v)

print('\n************************************************************************\n\nPositive:')
for key, value in disp.items():
    print()
    print(key)
    for v in value:
        if v[0][3:] == v[1][:3]:
            print(f'{v[0][:3]}{v[1][3:]}', end=' ')
            print(v)
print('\n************************************************************************\nDone!:\n')

