# olmonopolet-api
API with beer data from Vinmonopolet. Data includes stores, products, prices, stock and ratings


# Available Endpoints

**Beer**  
All beers to have been in stock on Vinmonopolet  
```http
[GET]
api/v1/beers
```
----------
**Stores**  
Retrieve all Vinmonopolet stores  
```http
[GET]
api/v1/stores
```

----------
**Stock**  
Beer stock in all Vinmonopolet stores
```http
[GET]
api/v1/beer-stock
```
Query Parameters:  
*[store_id]: int*  -  Provide store_id to get all stock for that store.  
*[beer_id]:int*  -  Provide beer_id to get all stock in stores for that beer.  

----------

**Sales**  
Daily beer sales for Vinmonopolet stores
```http
[GET]
api/v1/sales/daily
```
Query Parameters:  
*[store_id]: int*  -  Provide store_id to get daily beer sales for given store.  
*[beer_id]:int*  -  Provide beer_id to get daily sales per store for given beer.   
*[sales_day]:str*  -  Provide a date [yyyy-mm-dd] to filter results by sales date.  

----------

**Untappd**  
Beer Ratings from Untappd  
```http
[GET]
api/v1/untappd/rating
``` 
Query Parameters:  
*[beer_id]:int*  -  Provide beer_id to get rating for given beer.  


Verified beer mappings between Vinmonopolet and Untappd.
```http
[GET]
api/v1/untappd/mapping
``` 
Query Parameters:  
*[beer_id]:int*  -  Provide beer_id to get mapping for given beer.


# Disclaimer  
This work is by **no** means affiliated with Vinmonopolet or Untappd.