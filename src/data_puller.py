import csv
import requests
from multiprocessing import Pool
from dataclasses import dataclass, field
from collections import Counter
from datetime import datetime

@dataclass
class SiteStatus:
    link:    list = field(default_factory=list)
    blocked: bool = False 
    okay:    bool = False
    other:   bool = False
    errors:  bool = False


class DataPuller:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []
        self.read()
        
    def read(self): 
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                self.data.append(row)

    def checkurl(self, line):
        """multiprocessing worker function
        """
        status = SiteStatus()
        status.link = line
        try:
            r = requests.get(line[-1], timeout=30)
            if r.status_code == 403:
                status.blocked = True
            elif r.status_code == 200:
                status.okay = True
            else:
                status.other = True
        except:
            status.errors = True
        return status

    def process_presence_count(self):
        presence_counter = Counter()
        processing_pool = Pool(processes=20)
        results = processing_pool.map(self.checkurl, self.data)
        for thing in results:
            count_struct = {k: v for k, v in thing.__dict__.items() if k != 'link'}
            presence_counter.update(count_struct)
        return(presence_counter)

if __name__ == "__main__":
    pulled_data = DataPuller('../data/university_list.csv')
    presence_counter = pulled_data.process_presence_count()
    now = datetime.now()
    date_stuff = now.strftime("%Y:%m:%dT%H:%M:%S")
    print(f'{date_stuff},'
          f'{presence_counter["okay"]},'
          f'{presence_counter["blocked"]},'
          f'{presence_counter["errors"]},'
          f'{presence_counter["other"]}')
