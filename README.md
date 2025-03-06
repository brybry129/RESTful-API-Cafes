# RESTful API Cafes

This is a locally hosted RESTful API I built in Python using Flask and SQLAlchemy. It can be used to get, add, or delete information about cafes.

## Dependencies
This project requires a SQLAlchemy database named "cafes.db". To be able to use any of the GET functions you must first add info into the database. Please see the [POST Add a New Cafe](#POST-Add-a-New-Cafe) below. 

Install the modules needed:
```
python -m pip install -r requirements.txt
```

## API Documentation

### $${\color{green}GET}$$ Get All Cafes
Get a list of all cafes.

```
http://localhost/all
```

#### Sample JSON Response
```
{
    "cafes": [
        {
            "can_take_calls": true,
            "coffee_price": "£2.40",
            "has_sockets": true,
            "has_toilet": true,
            "has_wifi": false,
            "id": 1,
            "img_url": "https://atlondonbridge.com/wp-content/uploads/2019/02/Pano_9758_9761-Edit-190918_LTS_Science_Gallery-Medium-Crop-V2.jpg",
            "location": "London Bridge",
            "map_url": "https://g.page/scigallerylon?share",
            "name": "Science Gallery London",
            "seats": "50+"
        }
    ]
}
```

### $${\color{green}GET}$$ Get Random Cafe
Get a random cafe.

```
http://localhost/random
```

#### Sample JSON Response
```
{
    "cafes": [
        {
            "can_take_calls": true,
            "coffee_price": "£2.40",
            "has_sockets": true,
            "has_toilet": true,
            "has_wifi": false,
            "id": 1,
            "img_url": "https://atlondonbridge.com/wp-content/uploads/2019/02/Pano_9758_9761-Edit-190918_LTS_Science_Gallery-Medium-Crop-V2.jpg",
            "location": "London Bridge",
            "map_url": "https://g.page/scigallerylon?share",
            "name": "Science Gallery London",
            "seats": "50+"
        }
    ]
}
```

### $${\color{green}GET}$$ Search Cafes by Location
Get a cafe by location

```
http://localhost/search
```
#### Parameters
loc (string)

Example: ``` GET /search?loc=city ```

#### Sample JSON Response
```
{
    "cafes": [
        {
            "can_take_calls": true,
            "coffee_price": "£2.40",
            "has_sockets": true,
            "has_toilet": true,
            "has_wifi": false,
            "id": 1,
            "img_url": "https://atlondonbridge.com/wp-content/uploads/2019/02/Pano_9758_9761-Edit-190918_LTS_Science_Gallery-Medium-Crop-V2.jpg",
            "location": "London Bridge",
            "map_url": "https://g.page/scigallerylon?share",
            "name": "Science Gallery London",
            "seats": "50+"
        }
    ]
}
```

### $${\color{orange}POST}$$ Add a New Cafe
Add a new cafe

```
http://locahost/add
```
#### Body urlencoded
can_take_calls (string)
coffee_price (float)
has_sockets (string)
has_toilets (string)
has_wifi (string)
img_url (string)
location (string)
map_url (string)
name (string)
seats (int)

#### Sample JSON Response
```
{
    "response": {
        "success": "Successfully added the new cafe."
    }
}
```

### $${\color{purple}PATCH}$$ Update Price
Update the price of coffee for a cafe

```
http://locahost/update-price/<cafe_id>
```
#### Parameters
updated_price (float)

#### Sample JSON Response
```
{
    "success": "Successfully updated the price."
}
```

### $${\color{red}DELETE}$$ Delete Cafe
Delete a cafe. Requires API key, for testing purposes key is "1234"

```
http://locahost/cafe-closed/<cafe_id>
```
#### Parameters
api_key (int)

#### Sample JSON Response
```
{
    "success": "Successfully deleted the cafe."
}
```
