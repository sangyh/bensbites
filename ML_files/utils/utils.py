import requests
from bs4 import BeautifulSoup
import json
import openai
import pinecone
import json
import os
import numpy as np
import pandas as pd

ROOT_DIR = os.path.abspath('/home/sangy/Desktop/SideProjects/BensBites/bensbites')

if (os.environ.get("OPENAI_API_KEY") == None):
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT_DIR,'ML_files', 'config', 'conf', '.env')) #UPDATE PATH

openai.api_key = os.getenv("OPENAI_API_KEY")

# initialize connection to pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment="us-east1-gcp"
)


# create embeddings in pinecone db
# check if 'bensbitesDB' index already exists (only create index if not)
if 'bensbitesposts' not in pinecone.list_indexes():
    pinecone.create_index('bensbitesposts', dimension=1536)
# connect to index
index = pinecone.Index('bensbitesposts')

def extract_data_from_page(pageno, send_post_volume = False):
    # Set the URL of the request
    network_url = "https://www.bensbites.co/posts?page=" + str(pageno) + "&_data=routes%2F__loaders%2Fposts"
    print(network_url)
    # Set the request headers
    headers = {
        "User-Agent": "Chrome/108.0.0.0",
        "Accept-Language": "en-US"
    }

    # Send the request and retrieve the response
    response = requests.get(network_url, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        # The request was successful, so you can parse the response content
        content = response.content
        
        # Parse the response content as JSON
        content_json = json.loads(content)

        if send_post_volume:
            return content_json['pagination']

    else:
        # The request was not successful, so handle the error
        print("An error occurred:", response.status_code)

    return content_json


def extract_urls(e):
    section_urls=[]
    try:
        links =  e.find_all('a')
        
        text, href = [],[]
        for link in links:
            try:
                text.append(link.get_text())
                href.append(link.get("href"))
            except:
                text.append("N/A")
                href.append("N/A")
        section_urls = list(zip(text, href))
        
    except:
        pass
    return section_urls

    
def read_post(url, verbose=False):
    ''' 
    header
    -- section 
    '''
    print(url)
    
    
    post_data = {} #store all needed infor from the post url
    

    # Make a request to the website
    response = requests.get(url)

    # Parse the HTML content of the website
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main content element of the blog post
    main_content_element = soup.find('div', id='content-blocks')

    # Find all the h1, h2, h3, etc. elements within the main content element
    header_elements = main_content_element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    
    #iterate across all sections
    for element in header_elements:
        section_data = [] #list of all info from this seciton
        section_urls = []

        # Extract the text from the header element
        header_text = element.get_text()  
        # Find the next header element
        next_header_element = element.find_next(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']).get_text()
    

        divs = element.parent.find_next_siblings('div')
        
        for div in divs:

            if div.get_text() == next_header_element:
                #if verbose:
                #    print('<--NEXT HEADER REACHED-->')
                #    print('----> Next header:', div.get_text())
                break
            
            # If the div contains a ul (unordered list) element,extract the text from each li (list item) element separately
            if div.find('ul'):
                for li in div.find_all('li'):
                    section_data.append(li.text)
                    section_urls.append(extract_urls(li))
            else:
                section_data.append(div.text)
                section_urls.append(extract_urls(div))

        # Add the text list to the dictionary under the current header
        post_data[header_text] = list(zip(section_data,section_urls))
    
    return post_data

def assign_topics_gpt3(query, topicid2labels):

    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Following are topics for a database of news snippets from a artifical intelligence newsletter.\nIt is formatted as key-value pairs representing as id-name pairs.\n\n " + str(topicid2labels) + "\n\nFor any new news snippet, classifiy it to a topic for the list above. If nothing matches, create a new topic.\n\nSnippet: 'MusicLM: Generating Music From Text, via Google.'\nTopic: Music Generation/Audio Synthesis\n\nSnipeet: " + query + "\nTopic:",
                    temperature=0.7,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

    return (response.choices[0].text, response.usage.total_tokens)

     
def compress_json(url, data):
    cols=['url','section','item']
    tmp = pd.DataFrame(columns=cols)


    for section, contents in data[url].items():
        for item in contents:
            if len(item)==0:
                continue
    
            tmp = pd.concat([tmp, pd.DataFrame(np.array([url, section, item],dtype='object' ).reshape(1,-1), columns=cols)],ignore_index=True, axis=0)
    return tmp

def create_post_embeddings(df):
    count = 0  # we'll use the count to create unique IDs
    batch_size = 32  # process everything in batches of 32
    for i in range(0, len(df['item_text']), batch_size):
        # set end position of batch
        i_end = min(i+batch_size, len(df['item_text']))
        # get batch of lines and IDs
        lines_batch = df['item_text'][i: i+batch_size].tolist()
        ids_batch = [str(n) for n in range(i, i_end)]
        # create embeddings
        res = openai.Embedding.create(input = lines_batch, model='text-embedding-ada-002')
        
        embeds = [record['embedding'] for record in res['data']]
        # prep metadata and upsert batch
        meta = [{'text': line} for line in lines_batch]
        to_upsert = zip(ids_batch, embeds, meta)
        # upsert to Pinecone
        index.upsert(vectors=list(to_upsert))


#Query embeddings
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   try:
    res = openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
    return res
   except:
    print('Text not being embedded:', text)
    pass 


def search_items(df, query, n=5):
   embedding = get_embedding(query, model='text-embedding-ada-002')
   res = index.query([embedding], top_k=n, include_metadata=True)
    
   res_index = [(int(item.id), item.score) for item in res['matches']] 
   res_df = df.loc[[x[0] for x in res_index]][['url', 'section','item_text','item_url']]
   res_json = res_df.to_json(orient = "records")

   return res_json
 
def filter_items(df, topic, n=10):
    res_df = df[df.topic==topic][['url', 'section','item_text','item_url']]
    res_json = res_df.to_json(orient = "records")
    print(topic)
    print(df.topic.unique())
    print('res:', res_df)
    return res_json
