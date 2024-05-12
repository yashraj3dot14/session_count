import pandas as pd
from os.path import abspath,expanduser



def calc_session_time(path):
    users_list = ['ALICE99', 'CHARLIE']
    marker = ['start', 'end']

    try:
        final_path = abspath(expanduser('~/') + path)
        df = pd.read_csv(final_path, sep= ' ', names= ['timestamp', 'user', 'marker'])
    except:
        print('!!! File does not exist at provided file path')
        return None, None

    df['timestamp'] = pd.to_datetime(df.timestamp, errors= 'coerce')
    df['marker'] = df['marker'].str.lower()

    df = df[(~df['timestamp'].isna()) & (df['user'].isin(users_list)) & (df['marker'].isin(marker))]

    general_start_time = df['timestamp'].iloc[0]
    general_end_time = df['timestamp'].iloc[len(df)-1]

    record_map = {}
    for user in users_list:
        record_map[user] = {'session': 0, 'timestamp': 0}

    df['visited'] = None
    for index, data in df.iterrows():
        if data['visited'] != True:
            user = data['user']
            marker = data['marker']
            timestamp1 = data['timestamp']

            if marker == 'start':
                desired = 'end'
            else:
                desired = 'start'

            for inner_index, inner_data in df.iterrows():
                if inner_index > index and inner_data['visited'] != True and \
                    inner_data['marker'] == desired and inner_data['user'] == user:

                    df.loc[inner_index, 'visited'] = True
                    df.loc[index, 'visited'] = True
                    timestamp2 = inner_data['timestamp']
                    total_time = (timestamp2 - timestamp1).total_seconds()

                    record_map[user]['timestamp'] = record_map[user]['timestamp'] + int(total_time)
                    record_map[user]['session'] = record_map[user]['session'] + 1
                    break


    #no end or start available available
    end_df = df[(df['visited'] != True)& (df['marker'] == 'end')]
    start_df = df[(df['visited'] != True)& (df['marker'] == 'start')]

    #calculation for no start time mentioned
    for index, data in end_df.iterrows():
        end_time = data['timestamp']
        user = data['user']
        total_time = (end_time - general_start_time).total_seconds()
        record_map[user]['timestamp'] = record_map[user]['timestamp'] + int(total_time)
        record_map[user]['session'] = record_map[user]['session'] + 1

    #calculation for mp end time mentioned
    for index, data in start_df.iterrows():
        start_time = data['timestamp']
        user = data['user']
        total_time = (general_end_time - start_time).total_seconds()
        record_map[user]['timestamp'] = record_map[user]['timestamp'] + int(total_time)
        record_map[user]['session'] = record_map[user]['session'] + 1

    return record_map, users_list


def print_record(res, user_list):
    for user in user_list:
        op = user + ' ' + str(res[user]['session']) + ' ' + str(res[user]['timestamp'])
        print(op)

if __name__ == '__main__':
    path = input('enter path: ')
    res, user_list = calc_session_time(path)
    if res:
        print_record(res, user_list)

