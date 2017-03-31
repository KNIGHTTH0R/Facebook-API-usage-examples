#L. Bellinger 2017
import facebook
import requests

app_id = 'your_app_id'
my_token = 'your_app_token'

graph = facebook.GraphAPI(access_token=my_token, version='2.7')

search_query = 'your search query'
pages_results = graph.request('/search?q=%s&type=page&limit=100' % (search_query))


# ---- Getting the pages' IDs ----
all_pages_ids=[]
while True:
    try:
        for page in pages_results['data']:
            #page name and page ID are available
            all_pages_ids.append(page['id'])
            
        # Attempt to make a request to the next page of data, if it exists.
        pages_results=requests.get(pages_results['paging']['next']).json()
        
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the loop.
        break

# ---- Getting the pages' information ----
    
#maximum number of IDS allowed is 50 as of now.
if len(all_pages_ids)>50:
    pages_ids = list(all_pages_ids)

    while pages_ids:
        pages = graph.get_objects(ids=pages_ids[:50], fields='about,category,contact_address,current_location,description,emails,engagement, fan_count, general_info') #put the fields you'd like to get (https://developers.facebook.com/docs/graph-api/reference/page/)
        for id in pages_ids[:50]:
              #get whatever you need here and do whatever you want with!
        del pages_ids[:50]
else:
    pages = graph.get_objects(ids=all_pages_ids, fields='about,category,contact_address,current_location,description,emails,engagement, fan_count, general_info') #put the fields you'd like to get (https://developers.facebook.com/docs/graph-api/reference/page/)
    for id in all_pages_ids:
        #get whatever you need here and do whatever you want with!'''
            
all_posts=[]

# ---- Getting the pages' posts ID (can be merged with the previous step to limit API calls) ----
print("oui")
if len(all_pages_ids)>50:
    pages_ids = list(all_pages_ids)
    print(len(pages_ids))
    
    while pages_ids:

        pages = graph.get_objects(ids=pages_ids[2:4], fields='posts') #put the fields you'd like to get (https://developers.facebook.com/docs/graph-api/reference/page/)
        
        for id in pages_ids[2:4]:
            if len(pages[id])>= 2: #checks if a page has posted
                temp = pages[id]['posts']        
                
                while True:
                    try:
                        for post in temp['data']:
                            all_posts.append(post['id'])

                        # Attempt to make a request to the next page of data, if it exists.             
                        temp=requests.get(temp['paging']['next']).json()

                    except KeyError:
                        # When there are no more pages (['paging']['next']), break from the loop.
                        break
        del pages_ids[:50]

else: #this else part should be tested
    pages = graph.get_objects(ids=pages_ids[:50], fields='posts')
    for id in all_pages_ids:
                if len(pages[id])>= 2: #checks if a page has posted
                    temp = pages[id]['posts']        
                    
                    while True:
                        try:
                            for post in temp['data']:
                                all_posts.append(post['id'])

                            # Attempt to make a request to the next page of data, if it exists.             
                            temp=requests.get(temp['paging']['next']).json()

                        except KeyError:
                            # When there are no more pages (['paging']['next']), break from the loop and end the loop.
                            break
    

# ---- Getting the information for each post collected (can be merged with the previous step to limit API calls) ----
    
while all_posts:
    post_ = graph.get_objects(ids=all_posts[:50], fields='from,message,link') #put the fields you'd like to get (https://developers.facebook.com/docs/graph-api/reference/post)
    for id in all_posts[:50]:
        print(post_[id])
    del all_posts[:50]

#full code should be refactored: if len() else can be removed and position of "graph.etc" can be improved i guess
