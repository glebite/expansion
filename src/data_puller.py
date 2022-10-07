import csv
import requests
from multiprocessing import Pool


class DataPuller:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []

    def read(self): 
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                self.data.append(row)

def checkurl(line):
    try:
        r = requests.get(line[-1], timeout=10)
    except:
        print(f'URL error: {line[0]:60s} {line[-1]}')
    else:
        pass
    
def main():
    x = DataPuller('../data/university_list.csv')
    x.read()
    p = Pool(processes=20)
    result = p.map(checkurl, x.data)


if __name__ == "__main__":
    main()
