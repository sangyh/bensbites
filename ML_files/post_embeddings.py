import pandas as pd
from utils import utils
import json
import os
import openai

ROOT_DIR = os.path.abspath('/Users/sangyhan/Desktop/SideProjects/Arena/BensBites Semantic search/')

if (os.environ.get("OPENAI_API_KEY") == None):
 from dotenv import load_dotenv
 load_dotenv(os.path.join(ROOT_DIR,'openai', 'config', 'conf', '.env'))

openai.api_key = os.getenv("OPENAI_API_KEY")


### read slugs
all_slugs = []
with open('bensbites_slugs_dec17.txt') as f:
    for line in f:
        all_slugs.append(line.replace('\n',''))


### read posts json
f = open('bensbites_scraped_dec17.json')
data = json.load(f)
f.close()  


### compile json to df
cols=['url','section','item']
df = pd.DataFrame(columns=cols)
for slug in all_slugs:
    post_url = 'https://www.bensbites.co/p/' + slug
    tmp = utils.compress_json(post_url, data)
    df = pd.concat([df,tmp],ignore_index=True,axis=0) 

df['item_text'] = df['item'].apply(lambda x:x[0])
df['item_text_len'] = df['item_text'].apply(len)
df = df[df.item_text_len>0]
df['ada_embedding'] = df.item_text.apply(lambda x: utils.get_embedding(x, model='text-embedding-ada-002'))
df.to_csv('./embedded_bensbites_dec17.csv', index=False)

