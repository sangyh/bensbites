from utils import utils
import json
from post_embeddings import extract_posts
import os.path
### list of current slugs
curr_slugs=[]

ROOT_DIR = os.path.abspath('/home/sangy/Desktop/SideProjects/BensBites/bensbites')

# Read existing slug file
if os.path.isfile(os.path.join(ROOT_DIR, 'ML_files/bensbites_slugs.txt')):
    with open(os.path.join(ROOT_DIR, 'ML_files/bensbites_slugs.txt'), 'r') as f:
            data = f.read()
            curr_slugs = data.split('\n')
else:
    print('Creating new slug file')
    curr_slugs=[]

# The URL of the blog website
home_url =  'https://www.bensbites.co/'

### Extract post details
pagination_details = utils.extract_data_from_page(1, True)
tot_pages = pagination_details['total_pages']
tot_posts = pagination_details['total']
per_page = pagination_details['per_page']

#print(tot_pages, tot_posts, per_page)
#print(len(curr_slugs))

while True:
    if tot_posts==len(curr_slugs):
        print('No new posts added.')
        break

    posts_metadata = {}
    for page_no in range(tot_pages):
        content_json = utils.extract_data_from_page(page_no+1)
        posts_metadata[page_no+1] = content_json

    ### extract text in each post
    all_slugs=[]

    for page in range(tot_pages): #iterate over pages
        print(len(posts_metadata[page+1]['posts']))
        for post in posts_metadata[page+1]['posts']: #iterate over posts in each page
            all_slugs.append(post['slug'])

    new_slugs = set(all_slugs) - set(curr_slugs)

    ### read existing json
    if os.path.isfile(os.path.join(ROOT_DIR,'ML_files/bensbites_scraped.json')):
        with open(os.path.join(ROOT_DIR,'ML_files/bensbites_scraped.json'), 'r') as f:
            # Load the JSON data into a Python object
            bensbites_scraped = json.load(f)
    else:
        print('Creating new text-scraped json file')
        new_slugs = all_slugs
        bensbites_scraped={}
        

    ### save new slugs to txt file
    with open(os.path.join(ROOT_DIR, 'ML_files/bensbites_slugs.txt'), 'a') as f:
        for slug in new_slugs:
            f.write(f"{slug}\n")

    ### read new posts sequentially and write to json file
    for slug in new_slugs:
        post_url = 'https://www.bensbites.co/p/' + slug
        post_data = utils.read_post(post_url)
        bensbites_scraped[post_url] = post_data

    ### save to json
    with open(os.path.join(ROOT_DIR,'ML_files/bensbites_scraped.json'), 'w', encoding='utf-8') as f:
        json.dump(bensbites_scraped, f, ensure_ascii=False, indent=4)


    ### save new embeddings
    scraper = extract_posts()
    scraper.scrape(all_slugs)
    break

