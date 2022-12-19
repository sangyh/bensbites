
from ML_files.utils import utils
import pandas as pd
import os
import openai
from ast import literal_eval
from django.core.cache import cache

def load_file():
    print('Loading file')
    ### read embeddings
    df = pd.read_csv('ML_files/embedded_bensbites_dec17.csv')
    df.ada_embedding = df.ada_embedding.apply(literal_eval)
    df.item_url = df.item_url.apply(literal_eval)
    return df

def main(query):
    ROOT_DIR = os.path.abspath('./')

    if (os.environ.get("OPENAI_API_KEY") == None):
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT_DIR, 'ML_files', 'config', 'conf', '.env'))

    openai.api_key = os.getenv("OPENAI_API_KEY")

    df = cache.get('all_embeddings')
    if df is None:
        df = load_file()
        cache.set('all_embeddings', df, timeout=3600)
    print('File loaded')

    # Process the input and print the results
    results = utils.search_items(df, query, n=5)
    
    return results

if __name__ == '__main__':
  main()
