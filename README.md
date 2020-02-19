# Search API
A lightweight api to search for apartment listings in New York City.

## Environment
This is a Python 3 project. 

## Dependencies
* __Database:__ MongoDB
* __Database GUI:__ Mongodb Compass
* __API Package:__ Flask
* __Other Packages:__
    * Pymongo

## Instructions
To start the app, make sure all depedencies are properly installed. 

* __Setup DB:__ Connect to default local connection for mongo db in Compass. 
    * Create a database named ```rent-a-room```
    * Create a collection named ```Locations_NYC```
    * click on Add Data button to import the CSV file 
To run the app, input ```flask run```
use postman to send a post request at ```http://127.0.0.1:5000/```

example body:
    ```{"latitude": 40.7306, "longitude": -73.9352, "distance": 300.7}```

## Upcoming features
Query string match will be introduced to refine the search results further. 

## Author
Vasudha kalia
    

