# expansion  
It is now the expansion of an older tool to monitor university sites in Iran (for now)

## Introduction:
Knowledge is power.  It just is.  The Illegal Regime in Iran knows this.  They remember
how they enlisted the students back in 1979 to help with the unrest.  History is repeating
but now we can watch for when the government restricts access to the schools.  This toolset
helps with that.  Fork and improve!!!  

## Installation:
Clone the repo:  
> $ git clone https://github.com/glebite/expansion.git  

Cd into the repo:  
> $ cd expansion

Build a virtual environment and start installing the requirements:
(assuming Linux - sorry haven't tested with Windows yet)  
> $ python3 -m venv venv  
> $ source venv/bin/activate  
> $ python3 -m pip install -r requirements.txt  
(wait a bit)

## Workflow:
(assuming you're still in the venv from Installation)  
0) acquire the list of universities from a ranking site:
> $ cd src  
> $ python3 acquire_universities.py  
(this puts a university_list.csv file in to the local directory)  
> $ mkdir ../data  
> $ mv university_list.csv ../data  

1) pull the data goodness down:  
> $ python3 data_puller.py  
2022-10-10T11:50:27,128,120,60,3  

2) rinse and repeat OR setup crontab...  
> $ crontab -e
> (add)
> */15 * * * * /usr/bin/bash -c 'cd /home/luser/projects/expansion/src && source /home/luser/projects/expansion/venv/bin/activate && python3 /home/luser/projects/expansion/src/data_puller.py >> /home/luser/projects/expansion/data.txt'  

3) 



