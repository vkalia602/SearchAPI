#!/usr/bin/env python3
from flask import Flask, Response, request
from pymongo import MongoClient
from math import degrees, radians, cos, asin

app = Flask(__name__, instance_relative_config=True)

client = MongoClient()
db = client['rent-a-room']
collection = db['Locations_NYC']

# POST Endpoint for search api
@app.route('/', methods=['POST'])
def search():
    """
    POST endpoint for Search API. The endpoint expects a distance in meters for the search area for listings
    Optional parameters like Longitude and Latitude can be passed in for more refined results
    """
    #validate the body of request and set lat, lon and distance params
    lat, lon, distance = validateRequestAndSetVars(request.json)
    
    #rejecting request if distance not provided
    if distance == 'invalid request':
        return Response("{'invalid request': 'Distance is required'}", status=400)

    #finding the area in the distance radius from the provided/default lat and lon
    minLat, maxLat, minLon, maxLon = findLocation(lat, lon, distance)

    output = []
    defaultListings = []
    #querying mongodb to retrieve all the listings
    for query in collection.find():
        try:
            #extracting latitude and longitude from the listing
            q_lat = float(query['latitude'])
            q_lon = float(query['longitude'])
            #checking to see if lon and lat in the range of distance radius
            if (q_lat > minLat) and (q_lat < maxLat) and (q_lon > minLon) and (q_lon < maxLon):
                query['_id'] = str(query['_id'])
                output.append(query)
        #except errors in data type or values
        except(TypeError, ValueError): 
            continue
        #generating default listings if search fails to find any suitable listings
        if len(defaultListings) < 10:
            query['_id'] = str(query['_id'])
            defaultListings.append(query)
    #return the default list if search failed to find listings matching the parameters
    if len(output) == 0:
        output = defaultListings
    return {'listings': output}

def findLocation(lat, lon, rad):
    R = 6371
    maxLat = round(lat + degrees(rad/R), 5)
    minLat = round(lat - degrees(rad/R), 5)
    maxLon = round(lon + degrees(asin(rad/R) / cos(radians(lat))), 5)
    minLon = round(lon - degrees(asin(rad/R) / cos(radians(lat))), 5)

    return minLat, maxLat, minLon, maxLon

def validateRequestAndSetVars(requestBody):
    defaultLat = 40.64749
    defaultLon = -73.97237
    if 'distance' in requestBody:
        distance = float(requestBody['distance'] / 1000) #change into km
    else: 
        return 0, 0, 'invalid request'
    try:
        defaultLat = requestBody['latitude']
        defaultLon = requestBody['longitude']
    except KeyError:
        print('no key')

    return defaultLat, defaultLon, distance


if __name__ == '__main__':
    app.run(debug=True)