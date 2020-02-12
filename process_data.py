"""
Imports
"""
import pandas
import datetime
import numpy as np
from time import sleep
from hashmap import HashTable

ht = HashTable()


def load_data(filename, verbose=True):
    """ Preprocesses the data """

    timestamp = "timestamp"

    if verbose:
        print(f'Loading flyer dataset from {filename}')
    df = pandas.read_csv(filename)
    if verbose:
        print(f'\tReplacing null values in column flyer_id with 0')
    df['flyer_id'].replace(to_replace=np.nan, value=0, inplace=True)
    df['flyer_id'].replace(to_replace='%3Cnull%3G', value=0, inplace=True)
    if verbose:
        print(f'\tReplacing null values in column merchant_id with 0')
    df['merchant_id'].replace(to_replace=np.nan, value=0, inplace=True)

    return df


def get_user_ids(data):
    """ Gets the unique users IDs """

    user_id_col = data['user_id']
    return list(
        set(user_id_col)), {u_id: []
                            for u_id in list(set(user_id_col))}


def convert_time(t):
    """ Converts time to seconds """

    tm, _ = t.split('T')[1].split('-')
    hr, mn, sc = tm.split(':')
    delta = datetime.timedelta(hours=int(hr))
    delta2 = datetime.timedelta(hours=int(hr),
                                minutes=int(mn),
                                seconds=int(sc))
    tmer = delta2 - delta
    h, m, s = str(tmer).split(':')
    seconds = datetime.timedelta(hours=int(h), minutes=int(m),
                                 seconds=int(s)).total_seconds()

    return int(seconds)


def algorithm(list_time):
    """
    calculates the different between points in a list
    """
    N = len(list_time)
    if N == 1:
        return 0.0

    total = 0
    while N != 0:
        last = N - 1

        if last == 0:
            break
        sec_last = last - 1
        v = list_time[last] - list_time[sec_last]
        total += v

        N -= 1
    return total


def update_hashtable(data):
    """ Updates the hashtable """

    for i in range(len(data['timestamp'])):
        u_id = data['user_id'][i]
        flyer_id = int(data['flyer_id'][i])
        timestamp = data['timestamp'][i]
        secs = convert_time(timestamp)

        if flyer_id > 0:
            ht.insert_hash(u_id, [])
            value = ht.get(u_id)

            if isinstance(value, list):
                value += [secs]

            ht.insert_hash(u_id, value)
