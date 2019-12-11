import pandas as pd
import time

class TopUser:
    def __init__(self):
        self.data = pd.read_csv("tweets.csv")
        del self.data['html']
        del self.data['url']
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp']).astype(int)
        self.coinData = pd.read_csv("bitcoin-historical-data/bitstampUSD_1-min_data_2012-01-01_to_2019-08-12.csv")
        self.persons_df = pd.DataFrame(columns=['name','likes_mean','retweets_mean','replies_mean'])
        pass
    def insert(self, row):
        insert_loc = self.persons_df.index.max()
        if pd.isna(insert_loc):
            self.persons_df.loc[0] = row
        else:
            self.persons_df.loc[insert_loc + 1] = row
    
    def get_top_user_list(self):
        i=0
        data_group  = self.data.groupby(['user'])
        print(len(data_group))
        start = time.time()
        for name, group in data_group:
            self.insert([name,group['likes'].mean(),group['retweets'].mean(),group['replies'].mean()])
            i=i+1
            # increase this while deployment to len(data_group)
            if i==10000:
                break
        end = time.time()
        #print(self.persons_df.head(),end-start)
        self.persons_df = self.persons_df.sort_values(by=['likes_mean', 'retweets_mean','replies_mean'],ascending=False)
        result = self.persons_df.head(10)
        top_list = []
        for index,row in result.iterrows():
            top_list.append(row['name'])
        return top_list

tp = TopUser()

print(tp.get_top_user_list())