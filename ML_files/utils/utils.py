import requests
from bs4 import BeautifulSoup
import json
import openai
import json
import os
import numpy as np
import pandas as pd
from openai.embeddings_utils import cosine_similarity
 
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


def compress_json(url, data):
    cols=['url','section','item']
    tmp = pd.DataFrame(columns=cols)


    for section, contents in data[url].items():
        for item in contents:
            if len(item)==0:
                continue
    
            tmp = pd.concat([tmp, pd.DataFrame(np.array([url, section, item],dtype='object' ).reshape(1,-1), columns=cols)],ignore_index=True, axis=0)
    return tmp


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']



def search_items(df, query, n=5, pprint=True):
   embedding = get_embedding(query, model='text-embedding-ada-002')
   df['similarity'] = df.ada_embedding.apply(lambda x: round(cosine_similarity(x, embedding)*100,2))
   res = df[['url', 'section','item_text','item_url','similarity']].sort_values('similarity', ascending=False).head(n).to_json(orient = "records")
   return res
 
