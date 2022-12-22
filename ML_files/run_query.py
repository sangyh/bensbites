
from ML_files.utils import utils
import pandas as pd
import os
import openai
from ast import literal_eval
from django.core.cache import cache

def load_file():
    print('Loading file')
    ### read embeddings
    df = pd.read_csv('ML_files/embedded_bensbites_dec20.csv')
    df.ada_embedding = df.ada_embedding.apply(literal_eval)
    df.item_url = df.item_url.apply(literal_eval)
    return df

def load_topics():
    print('Loading topics file')
    ### read embeddings
    topics_df = pd.read_csv('ML_files/item_topics.csv')

    print(topics_df.columns)
    return topics_df

def main(query):
    ROOT_DIR = os.path.abspath('./')

    if (os.environ.get("OPENAI_API_KEY") == None):
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT_DIR, 'ML_files', 'config', 'conf', '.env'))

    openai.api_key = os.getenv("OPENAI_API_KEY")

    df = cache.get('all_embeddings')
    topics_df = cache.get('all_topics')
    if df is None:
        df = load_file()
        topics_df = load_topics()
        cache.set('all_embeddings', df, timeout=3600)
        cache.set('all_topics', topics_df, timeout=3600)
    print('File loaded')


    if query=='':
        results = df[['url', 'section','item_text','item_url']].head(10).to_json(orient = "records")
        
    else:
        # Process the input and print the results
        results, topic_ind = utils.search_items(df, query, n=5)
        print(topic_ind)
        topics = topics_df[topics_df['index'].isin(topic_ind)]['topic']
        print(topics)
    return results

if __name__ == '__main__':
  main()
