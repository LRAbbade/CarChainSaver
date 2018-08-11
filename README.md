# Car Chain Saver

This project gets the mileage from a [Car Simulator](https://github.com/LRAbbade/Car_Simulator) instance and saves it in the [CarChain Blockchain](https://github.com/alissonfpmorais/blockchain-js).

## Instructions

Make a `db_connector.py` file with a `get_mongo_client` function, which should return a `MongoClient` to your Database.

There should also be a `endpoint_ip.py` file with a `endpoint_ip` `str`, the `ip` of any [CarChain](https://github.com/alissonfpmorais/blockchain-js) node capable of hashing a block.

## Requirements:

| Library		   | Version   |
|-----------------:|:---------:|
| geopy 		   | 1.16.0	   |
| pymongo 	       | 3.6.0	   |
| requests-futures | 0.9.7	   |
