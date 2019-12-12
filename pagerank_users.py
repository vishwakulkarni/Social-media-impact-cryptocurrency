import re
import pandas as pd 
from operator import itemgetter


class PageRank:
    def __init__(self):
        self.df = pd.read_csv("tweets.csv")
        self.df['mention'] = self.df.text.str.findall(r'(?<![@\w])@(\w{1,25})').apply(str)
        self.df = self.df[self.df['mention'] != '[]']
        del self.df['html']
        del self.df['url']
    
    def parse_tweets(self):
        mentions = {}
        users = {}
        for index,row in self.df.iterrows():
            mentions[row['tweet-id']] = row['mention']
            users[row['tweet-id']] = row['user']
            if index == 5:
                print(mentions)
        return mentions,users

    def generate_graph_structure(self,mentions,users):
        #key: userID; value: mentioned userIDs
        graph_structure = {}
        unique_user_screen_names = set()
        # generate users nodes graph
        for tweet_id in mentions:
            user_screen_name = users[tweet_id]
            mentioned_userList = mentions[tweet_id]
            mentioned_userList = mentioned_userList.strip('][').split(', ')
            #print(mentioned_userList)
            for i in range(len(mentioned_userList)):
                mentioned_userList[i] = mentioned_userList[i].strip("'")
            for mentioned_user in mentioned_userList:
                mentioned_user_screen_name = mentioned_user
                if user_screen_name not in graph_structure:
                    graph_structure[user_screen_name] = []
                if mentioned_user_screen_name not in graph_structure[user_screen_name]: 
                    graph_structure[user_screen_name].append(mentioned_user_screen_name)
                unique_user_screen_names.add(mentioned_user_screen_name)
        new_users = unique_user_screen_names - set(graph_structure.keys())
        for user_screen_name in new_users:
            graph_structure[user_screen_name] = []
        
        return graph_structure

    def calculate_pagerank(self,graph_structure):
        ranked_users = {}
        pre_pagerank = {}
        cur_pagerank = {}
        error = 0.0
        for user_screen_name in graph_structure:
            pre_pagerank[user_screen_name] = 1.0
            cur_pagerank[user_screen_name] = 0.0
            error += abs(pre_pagerank[user_screen_name] - cur_pagerank[user_screen_name])
        while error > 10 ** (-6):
            for user_screen_name in cur_pagerank:
                cur_pagerank[user_screen_name] = 0.0
            # error should be 0.0 when every iteration begins
            error = 0.0
            # update the cur_pagerank from the pre_pagerank
            for user_screen_name in graph_structure:
                for mentioned_user_screen_name in graph_structure[user_screen_name]:
                    #if mentioned_userID not in cur_pagerank:
                    #cur_pagerank[mentioned_userID] = 0.0
                    if len(graph_structure[user_screen_name]) != 0:
                        cur_pagerank[mentioned_user_screen_name] += pre_pagerank[user_screen_name] / len(graph_structure[user_screen_name])
            #print cur_pagerank
            # update cur_pagerank with teleporting:
            for user_screen_name in cur_pagerank:
                cur_pagerank[user_screen_name] = 0.9 * cur_pagerank[user_screen_name] + 0.1 * (1.0 / float(len(graph_structure)))
                error += abs(pre_pagerank[user_screen_name] - cur_pagerank[user_screen_name])
            # when iteration finish, pre_pagerank store the result from cur_pagerank for next iter
            temp_dict = pre_pagerank
            pre_pagerank = cur_pagerank
            cur_pagerank = temp_dict

        #normalization
        max_pagerank = max(pre_pagerank.values())
        for user_screen_name in pre_pagerank:
            pre_pagerank[user_screen_name] = pre_pagerank[user_screen_name] / max_pagerank 
        # rank and output
        ranked_users = sorted(
            pre_pagerank.items(), key = itemgetter(1), reverse = True)
        ranked_users = ranked_users[:min(len(ranked_users), 50)]
        return ranked_users


#user below code for testing pageRank algorithm and extracting graph
#reference : https://github.com/karenxi/tweet_ranking_system

'''pr = PageRank()
mentions,users = pr.parse_tweets()
graph_structure = pr.generate_graph_structure(mentions,users)
#print(graph_structure)
Top_users = {}
for i in graph_structure:
    if len(graph_structure[i])>5:
        Top_users[i] = graph_structure[i]
print(Top_users)
print('ranked_users',pr.calculate_pagerank(graph_structure))'''