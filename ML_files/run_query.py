
from ML_files.utils import utils
import pandas as pd
import json
import os
import openai
import argparse
from ast import literal_eval

def main(query):
    ROOT_DIR = os.path.abspath('./')

    if (os.environ.get("OPENAI_API_KEY") == None):
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT_DIR, 'ML_files', 'config', 'conf', '.env'))

    openai.api_key = os.getenv("OPENAI_API_KEY")

    ### read embeddings
    df = pd.read_csv('ML_files/embedded_bensbites_dec17.csv')
    df.ada_embedding = df.ada_embedding.apply(literal_eval)


    # Process the input and print the results
    results = utils.search_items(df, query, n=3)
    
    return results

if __name__ == '__main__':
  main()
