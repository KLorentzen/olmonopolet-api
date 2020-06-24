from bs4 import BeautifulSoup
import httpx

def get_rating(url):
    '''
    Retrieve Untappd beer rating data

    Parameters:
    url: Untappd URL for the beer rating data

    Returns:
    dict: Dictionary with rating data
    '''

    beer_rating = {}

    # Get the web page where the Untappd beer rating data is and parse it using BeautifulSoup
    raw_untappd_response = httpx.get(url)
    untappd_html = BeautifulSoup(raw_untappd_response,'html.parser')

    # Retrieve Data

    beer_rating["rating"] = untappd_html.find("div", class_="content").find("div",class_="details").find("div",class_="caps")['data-rating']
    # Text is typically 'xxx Ratings', hence I need to split the string and get the first element
    beer_rating["num_regs"] = untappd_html.find("div", class_="content").find("div",class_="details").find("p",class_="raters").string.split()[0]
    beer_rating["check_in_total"] = untappd_html.find("div",class_="content").find("div",class_="stats").find("span",class_="count").string
    beer_rating["check_in_unique"] = untappd_html.find("div",class_="content").find("div",class_="stats").find_all("span",class_="count")[1].string
    # TODO: Add validations and try/excepts

    # Stripping thousand separator ',' from numbers
    beer_rating["num_regs"] = beer_rating["num_regs"].replace(',','')
    beer_rating["check_in_total"] = beer_rating["check_in_total"].replace(',','')
    beer_rating["check_in_unique"] = beer_rating["check_in_unique"].replace(',','')


    return beer_rating