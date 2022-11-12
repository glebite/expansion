"""graph.py

Convert the data read in into pandas dataframe and then
graph out the criteria over time.

Also dump out min/max for all time, min/max for
recent data and the current reading for Down.

"""
import time
import pandas as pd
from matplotlib import pyplot as plt


def extract_min_max(cdf):
    """Extract max and min values for 'Down' in a dataframe.

    Parameters:
    cdf (DataFame): contains the data to focus on

    Returns:
    min (int): minimum value from the input data
    max (int): maximum value from the input data
    """
    df2 = cdf.loc[cdf['Down'].idxmax()]
    df3 = cdf.loc[cdf['Down'].idxmin()]
    max = df2['Down']
    min = df3['Down']
    return min, max


EIGHT_HOURS = 4 * 8
LAST_ENTRY = 1


def main():
    """
    Essentially, open up the file, and then look at the last 8 hours.

    Plot the Okay, Blocked, Down, and Other fields.

    Text output of mins, max, and values.
    """
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    offset = offset / 60 / 60 * -1
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    df = pd.read_csv("../data.txt", header=None)
    df.columns = ['Date', 'Okay', 'Blocked', 'Down', 'Other']
    partial_df = df.tail(EIGHT_HOURS)
    last_df = df.tail(LAST_ENTRY)
    partial_df.plot(x='Date', y = ['Okay', 'Blocked', 'Down', 'Other'])
    plt.grid()
    plt.title('Criteria over time')
    plt.ylabel('Criteria count')
    plt.xlabel(f'Time (GMT{offset})')
    plt.xticks(rotation=90)
    plt.legend(loc=(1.04, 0))
    plt.savefig('graph.png')
    min, max = extract_min_max(partial_df)
    print(f'Recent    : {min=} {max=}')
    min, max = extract_min_max(df)
    print(f'Historical: {min=} {max=}')
    min, max = extract_min_max(last_df)
    print(f'Latest    : {max=}')
    

if __name__ == "__main__":
    main()

