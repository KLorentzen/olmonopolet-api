from bs4 import BeautifulSoup
import httpx

def test():
    return 'test'

def get_details_web(url):
    '''
    Retrieve Vinmonopolet beer details from the web

    Parameters:
    url: Vinmonopolet URL path for the beer (excl. www.vinmonopolet.no)

    Returns:
    dict: Dictionary with beer data - keys: style, alcohol, brewery
    '''
    VMP_BASE_URL = 'https://www.vinmonopolet.no'

    beer_details = {}

    # Get the web page of the beer (Vinmonopolet) and parse it using BeautifulSoup
    raw_vmp_response = httpx.get(f"{VMP_BASE_URL}{url}")
    untappd_html = BeautifulSoup(raw_vmp_response,'html.parser')

    # Scrape Data from Product page on Vinmonopolet
    beer_details['alcohol'] = untappd_html.find("ul", class_="product__contents-list").find("span", class_='product__contents-list__content-percentage').string

    for tab in untappd_html.find_all("ul", class_="product__tab-list"):
        
        for detail in tab.find_all('li'):
            
            product_info_category = detail.find('span', class_='product__tab-list__label').string
            if product_info_category == 'Varetype':
                beer_details['style'] = detail.find('span', class_='product__tab-list__value').get_text()
            elif product_info_category == 'Produsent':
                beer_details["brewery"] = detail.find('span', class_='product__tab-list__value').get_text()

    
    # Modify and clean product details 
    beer_details['style'] = beer_details['style'].replace('\n','').replace('\t','').replace('Øl, ','')
    beer_details['brewery'] = beer_details['brewery'].replace('\n','').replace('\t','')
    beer_details['alcohol'] = beer_details['alcohol'].replace('%','')


    return beer_details