from utils import utils
import json

# The URL of the blog website
home_url =  'https://www.bensbites.co/'

### Extract post details
pagination_details = utils.extract_data_from_page(1, True)
tot_pages = pagination_details['total_pages']
tot_posts = pagination_details['total']
per_page = pagination_details['per_page']

print(tot_pages, tot_posts, per_page)

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

### read posts sequentially
bensbites_scraped = {}
for slug in all_slugs:
    post_url = 'https://www.bensbites.co/p/' + slug
    
    post_data = utils.read_post(post_url)
    bensbites_scraped[post_url] = post_data

### save all slugs to csv
with open('bensbites_slugs_dec17.txt', 'w') as f:
    for slug in all_slugs:
        f.write(f"{slug}\n")

### save to json
with open('bensbites_scraped_dec17.json', 'w', encoding='utf-8') as f:
    json.dump(bensbites_scraped, f, ensure_ascii=False, indent=4)
