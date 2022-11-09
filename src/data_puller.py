"""data_puller

This tool is the important part of the whole system: 

Take a list of URLs and attempt to access the webpage 
and mark whether or not a site can be reached with 200 OK,
403 (IP blocked - for now), Down, or Other.

It does this as quickly as possible and then spits out 
the aggregated output.
"""
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
        """ initializer
        
        This code will attempt to read the file during
        creation.

        Parameters:
        file_name (str): the name of the file

        Returns:
        n/a
        """
        self.file_name = file_name
        self.data = []
        self.rates = {}
        self.read()
        
    def read(self):
        """ read - read in the contents of the data file """
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                self.data.append(row)

    def checkurl(self, line):
        """multiprocessing worker function
        """
        status = SiteStatus()
        status.link = line
        url = line[-1]
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 403:
                status.blocked = True
            elif r.status_code == 200:
                # TODO: capture b/s on a success - is the speed
                #       degradaded?
                status.okay = True
            else:
                status.other = True
        except:
            status.errors = True
        return status

    def process_presence_count(self):
        """process_presence_count
        """
        presence_counter = Counter()
        processing_pool = Pool(processes=300)
        results = processing_pool.map(self.checkurl, self.data)
        for thing in results:
            count_struct = {k: v for k, v in thing.__dict__.items() if k != 'link'}
            presence_counter.update(count_struct)
        return(presence_counter)


if __name__ == "__main__":
    # TODO: move to a "main" function
    # TODO: location pointer, config file location?
    pulled_data = DataPuller('../data/university_list.csv')
    presence_counter = pulled_data.process_presence_count()
    now = datetime.now()
    date_stuff = now.strftime("%Y-%m-%dT%H:%M:%S")
    print(f'{date_stuff},'
          f'{presence_counter["okay"]},'
          f'{presence_counter["blocked"]},'
          f'{presence_counter["errors"]},'
          f'{presence_counter["other"]}')
