import pandas as pd

data = pd.read_csv("StockMetrixApp_tweets.csv", delimiter = '|')
cnt = 0
list_ = []
for index, row in data.iterrows():
    #print(data['text'])
    if 'signals' in row['text']:
        for t in row['text'].split():
            cnt+=1
            if '$' in t and cnt==1:
                list_.append(row)
        cnt = 0
        #print(row['text'])
df = pd.DataFrame(list_)
with open('sample_tweets.csv','w') as f:
        df.to_csv(f, sep=';')
print(cnt)
