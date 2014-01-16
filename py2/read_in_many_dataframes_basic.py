import pandas as pd
import os
import gc

columns = ['date_time', 'auction_id_64', 'user_id_64', 'brand_id', 'creative_id', 'actual_bid_price', 'biased_bid_price', 'bid_reject_reason', 'm_floor_id', 'ym_bias_id', 'bidder_id', 'buyer_member_id', 'seller_member_id', 'total_bid_modifier']

bid_list = pd.DataFrame()

first = True

for file in os.listdir('.'):
    if 'bid' in file:
        print file
        if first:
            all_bids = pd.read_table('.'+file, names=columns)
            all_bids = all_bids[['buyer_member_id', 'brand_id', 'actual_bid_price']]
            first = False
            print("Results after first File:")
            print(all_bids.describe())
            print(all_bids)
        else:
            all_bids = all_bids.append((pd.read_table('.'+file, names=columns))[['buyer_member_id', 'brand_id', 'actual_bid_price']], ignore_index=True)
            print(all_bids)
            gc.collect()

print("read in complete, now calculating")

print("Results after all Files:")
print(all_bids.describe())
print(all_bids)

'''
Results after all Files:
       buyer_member_id         brand_id  actual_bid_price
count  70691602.000000  70691602.000000   70691602.000000
mean       1321.822109     20874.262959          0.283358
std         225.695431     19374.188200          0.504981
min          25.000000         0.000000          0.000000
25%        1371.000000      4386.000000          0.074893
50%        1371.000000     15777.000000          0.188300
75%        1371.000000     37576.000000          0.369663
max        2077.000000    100033.000000        118.983508
<class 'pandas.core.frame.DataFrame'>
Int64Index: 70691604 entries, 0 to 70691603
'''