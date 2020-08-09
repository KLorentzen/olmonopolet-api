from bs4 import BeautifulSoup
import httpx

def get_beer_details(url):
    '''
    Retrieve Untappd beer details  

    Parameters:
    url: Untappd URL for the beer

    Returns:
    dict: Dictionary with rating data
    '''

    untappd_details = {}

    # Get the web page where the Untappd beer rating data is and parse it using BeautifulSoup
    raw_untappd_response = httpx.get(url)
    untappd_html = BeautifulSoup(raw_untappd_response,'html.parser')

    # Retrieve Data
    try:
        untappd_details["brewery"] = untappd_html.find("div",class_="content").find('div', class_='name').find('a').string
        untappd_details["brewery_url"] = untappd_html.find("div",class_="content").find('div', class_='name').find('a')['href']
        untappd_details["style"] = untappd_html.find("div",class_="content").find('div', class_='name').find('p', class_='style').string
        # TODO: Få inn description korrekt. Per nå er det problematisk å få kun tekst siden det også er en <a> tag i div.
        untappd_details["description"] = untappd_html.find("div", class_="content").find("div",class_="bottom").find("div",class_="desc").find("div",class_="beer-descrption-read-less").contents

        # TODO: Handle img_url which is placeholder for missing img at Untappd
        untappd_details["img_url"] = untappd_html.find("div",class_="content").find('a',class_ = 'label').find('img')['src'] 

        untappd_details["rating"] = untappd_html.find("div", class_="content").find("div",class_="details").find("div",class_="caps")['data-rating']
        # Text is typically 'xxx Ratings', hence I need to split the string and get the first element
        untappd_details["num_regs"] = untappd_html.find("div", class_="content").find("div",class_="details").find("p",class_="raters").string.split()[0]
        untappd_details["check_in_total"] = untappd_html.find("div",class_="content").find("div",class_="stats").find("span",class_="count").string
        untappd_details["check_in_unique"] = untappd_html.find("div",class_="content").find("div",class_="stats").find_all("span",class_="count")[1].string

        # TODO: Add validations and try/excepts

        # Stripping thousand separator ',' from numbers
        untappd_details["num_regs"] = untappd_details["num_regs"].replace(',','')
        untappd_details["check_in_total"] = untappd_details["check_in_total"].replace(',','')
        untappd_details["check_in_unique"] = untappd_details["check_in_unique"].replace(',','')
    except Exception as err:
        print(f"Exception cought while updating untappd data: {err}")


    return untappd_details