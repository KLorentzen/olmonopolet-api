import httpx
from bs4 import BeautifulSoup
import json
import itertools
import time


def _get_search_result_count(search_object):
    '''
    get number of results when searching for a beer at Untappd 

    Parameters:
    BeautifulSoup object

    Returns:  
    int: Number of search results
    '''
    try:
        for el in search_object.find_all('p', class_ ='total'):
            count = el.strong.string

        return int(count.replace(' beer',''))
    except UnboundLocalError:
        return 0

def _get_untappd_mapping_data(search_item):
    '''
    Pass in a Beautifulsoup html object representing a search on Untappd to return details about the search result.
    Returns data for the first search result on Untappd.com  
    
    Parameters:  
    Beautifulsoup object  
    
    Returns:
    dict: beer id, name and URL
    '''
    # Untappd beer object to return
    mapping_data = {
        'id':'',
        'url': '',
        'name': '',
    }

    _id = search_item.find("a",class_="label")["href"].replace('/beer/','')
    _url = search_item.find("div",class_="beer-details").find('p',class_ = 'name').find('a')['href'] 
    _name = search_item.find("div",class_="beer-item").find('p',class_ = 'name').find('a').string 
    
    mapping_data["id"]= int(_id)
    mapping_data["url"]='https://untappd.com' + _url
    mapping_data["name"]=_name

    return mapping_data


def clean_beer_name(beer_name):
    '''
    Pre-process beer name before searching for the given name on Untappd.com.  
    Parameters:  
    str: Beer name  
    Returns:  
    list: Processed beer name as list
    '''

    # Words to clean from beer name
    word_replacements = [
    {
        'replace': ' x ',
        'replace_with': ' '
    },
    {
        'replace': ',',
        'replace_with': ''
    },
    {
        'replace': ' & ',
        'replace_with': ' '
    },
    {
        'replace': '!',
        'replace_with': ''
    },
]
    for word in word_replacements:
        beer_name = beer_name.lower().replace(word['replace'],word['replace_with'])

    # Limiting number of search words to [6] for long beer names
    beer_name = beer_name.split()[:6] if len(beer_name.split()) > 7 else beer_name.split()


    return beer_name


def find_untappd_mapping(beer_name, current_search_count, search_limit):
    '''
    Obtain mapping between beer from Vinmonopolet and Untappd. Number of searches are limited according to set parameters.  
    Parameters:  
    string: Vinmonopolet beer name  
    int: Number of searches performed at the time when the method is called  
    int: The maximum number of searches allowed  

    Returns:  
    dict: beer id, name, URL and mapping status for beer at Untappd.com. Returns dictionary with id=0 and empty name and URL if not found.
    
    '''

    ####################################
    URL = "https://untappd.com/search"
    ####################################

    # Dictionary to return with mapping details on Untappd.com
    mapping_details = {
        'name':'',
        'id': 0,
        'url':'',
        'match': False,
        'searches': current_search_count
    }
    
    best_search = {
        'results' : 10000,
        'words' : []
    }

    beer_name = clean_beer_name(beer_name)

    word_count = len(beer_name)

    # Indicates if a mapping is successfully obtained with Untappd.com
    mapping_success = False
    

    for i in range(word_count):
        # List with all word combinations
        word_combinations = [list(word) for word in itertools.combinations(beer_name, word_count - i)]


        for words in word_combinations:
            query_words = ' '.join(words)

            # Search param for untappd
            PARAMS = {"q": query_words }

            # Check number of searches - exit if search count > limit
            current_search_count += 1
            mapping_details['searches'] = current_search_count
            if current_search_count > search_limit:
                return mapping_details

            print(f"Searching for: {query_words}, count ({current_search_count}/{search_limit})")

            # Perform query on Untappd using Word combinations from name on VMP
            response = httpx.get(URL,params=PARAMS)
            untappd_html = BeautifulSoup(response,'html.parser')
            

            if _get_search_result_count(untappd_html) == 1:
                
                mapping_details = _get_untappd_mapping_data(untappd_html)
                mapping_details['searches'] = current_search_count
                mapping_details['match'] = True
                mapping_success = True
                break
            else:
                if _get_search_result_count(untappd_html) < best_search['results']:
                    best_search['results'] = _get_search_result_count(untappd_html)
                    best_search['html'] = untappd_html

            # TODO: add more logic to find beer if it is not possible to find a single search result
            # Reduce request intensity towards Untappd.com
            time.sleep(1)

        if mapping_success:
            # Break if result is found
            break
    
    # if not mapping_success:
    #     mapping_details = _get_untappd_mapping_data(best_search['html'])
    #     print(f"Using best result with {best_search['results']} search results")

    return mapping_details