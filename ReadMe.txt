Run Project

1. docker compose up --build 

We must input Initial data: This is the address of the pizzas shop.

2. Migrate the pizza shop data by running
	- docker-compose run web /usr/local/bin/python manage.py makemigrations
	- docker-compose run web /usr/local/bin/python manage.py migrate

Let's Run the Server:
3. docker compose up


-----------------------------------------------------------------------------------------

Using PostMan


-----------------------------------------------------------------------------------------

To Run Test:

 1. docker-compose run web /usr/local/bin/python manage.py test delivery/test   


 -----------------------------------------------------------------------------------------


 Methodolgy

 - Approach

	For finding the optimal path, I used a standard lat/lng calculation to estimate the distance from point A - B.
	As a pizza shop we want to delivery most recent orders first... My goal is for the bot to deliver as many Pizzas as possible before having to go back to recharge. 

	As an approved approach I would also take into account the distance as well as the order time. To ensure the bot get the most orders each route. 
	For the sake of this iteration I determine the optimal path, was one in which we got the order out by order time. 

	- Database 
	 In this scenerio I determined the need for three databases.
	 	- Order: 
			This table holds the order that are parsed from the csv. 
			The database is ordered from the most recent order.
		    The post call, for returning the next address looks at the most recent order, or in the case of the database the first item.  
            Notes: 
			 Since I have a service for calculating distance, I would probably add a field that stores the distance from the pizza shop.
			 This would allow me to add more complexity to my routing, by determining the closest order to start from.
		- Delivery:	
		   This table is responsible for storing the states of the current delivery and remaining distance.  
		   The table is designed to work as a STACK (FIFO) as the remaining distance is calculating from the previous delivery.
		   It also tracks the states of being delivered. 
		   Notes:
		   One of the things I check for is if the delivery is in Range, instead of removing, I would have another field to track this. This 
		   could be valuable data to the company to identify new opportunities. 
		- FileUpload
		  Stores the file being uploaded   
			
    - Views
		The views utilizes separated services all provided in the services folder to parse file, calculate distances, and update objects.
		







	