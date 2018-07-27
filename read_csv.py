import pandas as pd

data = pd.read_csv("StockMetrixApp_tweets.csv", delimiter = '|')
cnt = 0
cnt2 = 0

for index, row in data.iterrows():
    #print(data['text'])
    if 'signals' in row['text']:
        print(row['text'])
        cnt+=1
print(cnt)
