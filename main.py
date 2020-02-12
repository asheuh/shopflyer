import process_data
from time import sleep
from pandas import DataFrame
from process_data import ht


def main():
    """ Run the main code for display """
    filename = 'Sampleflyerdataset.csv'

    data = process_data.load_data(filename)
    process_data.update_hashtable(data)
    users, _ = process_data.get_user_ids(data)

    number_of_users = len(users)
    total_number_of_flyers = 0

    user_l = []
    avg_list = []
    total_list = []

    for u_id in users:
        value = ht.get(u_id)
        if value:
            total = process_data.algorithm(sorted(value))
            al = len(value)
            avg = round(total / al, 1)
            print()

            print(
                f"|\tUser_ID: {u_id}\t|\tAverage Time on Flyer: {avg}Seconds\t|\tTotal Flyers: {al}"
            )
            sleep(0.3)

            user_l.append(u_id)
            avg_list.append(avg)
            total_list.append(al)

    data_frame = {
        'User ID': user_l,
        'Average Time On Flyer': avg_list,
        'Total Flyer': total_list
    }

    df = DataFrame(data_frame)
    df.to_excel('Report.xlsx', sheet_name='Sheet1', index=True)


if __name__ == '__main__':
    main()
