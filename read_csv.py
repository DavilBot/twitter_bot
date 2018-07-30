import pandas as pd

data = pd.read_csv("StockMetrixApp_tweets.csv", delimiter = '|')
cnt = 0
list_ = []
for index, row in data.iterrows():
    #print(data['text'])
    if 'signals' in row['text']:
        list_.append(row)
        print(row['text'])
        cnt+=1
df = pd.DataFrame(list_)
with open('sample_tweets.csv','w') as f:
        df.to_csv(f, sep=';')
print(cnt)
