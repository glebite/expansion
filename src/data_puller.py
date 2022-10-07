import csv
import requests


class DataPuller:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []

    def read(self): 
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                self.data.append(row)


def main():
    x = DataPuller('../data/university_list.csv')
    x.read()
    for line in x.data:
        try:
            r = requests.get(line[-1], timeout=10)
            print(r, line[0], len(r.text)/r.elapsed.total_seconds())
        except Exception as e:
            print(line[0], 'failure')
            pass



if __name__ == "__main__":
    main()
