# Project 3 - Web Programming with Python and JavaScript

## Overview
  In this project, you’ll build an web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

## Requirements
Alright, it’s time to actually build your web application! Here are the requirements:

- Menu: Your web application should support all of the available menu items for Pinnochio’s Pizza & Subs (a popular pizza place in Cambridge). It’s up to you, based on analyzing the menu and the various types of possible ordered items (small vs. large, toppings, additions, etc.) to decide how to construct your models to best represent the information. Add your models to orders/models.py, make the necessary migration files, and apply those migrations.
- Adding Items: Using Django Admin, site administrators (restaurant owners) should be able to add, update, and remove items on the menu. Add all of the items from the Pinnochio’s menu into your database using either the Admin UI or by running Python commands in Django’s shell.
- Registration, Login, Logout: Site users (customers) should be able to register for your web application with a username, password, first name, last name, and email address. Customers should then be able to log in and log out of your website.
Shopping Cart: Once logged in, users should see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their virtual “shopping cart.” The contents of the shopping should be saved even if a user closes the window, or logs out and logs back in again.
- Placing an Order: Once there is at least one item in a user’s shopping cart, they should be able to place an order, whereby the user is asked to confirm the items in the shopping cart, and the total (no need to worry about tax!) before placing an order.
- Viewing Orders: Site administrators should have access to a page where they can view any orders that have already been placed.
- Personal Touch: Add at least one additional feature of your choosing to the web application. Possibilities include: allowing site administrators to mark orders as complete and allowing users to see the status of their pending or completed orders, integrating with the Stripe API to allow users to actually use a credit card to make a purchase during checkout, or supporting sending users a confirmation email once their purchase is complete. If you need to use any credentials (like passwords or API credentials) for your personal touch, be sure not to store any credentials in your source code, better to use environment variables!

## Initialization
 - install dependencies with [pip install -r requirements.txt]
 - Make migrations with python manage.py makemigrations.
 - Apply migrations with python manage.py migrate.
 - Create superuser with python manage.py createsuperuser.
 - You can populate the database with menu items from by running python database.py.
## Database models
 - Size. Product variations item. After running populating script have two values: Small and Large.
 - Topping. Contains various toppings for pizza items.
 - SubAddon. Contains various addons for subs (Sorry, I don't know how to name these things properly).
 - PizzaName. Populating with two values: Regular and Sicilian.
 - Pizza. Pizza items themselves. Includes toppings_count field that can be 0, 1, 2, 3 or 5 for Special Pizza.
 - SubName. Contains all Subs names.
 - Sub. Subs themselves.
 - Pasta. A model for all pastas.
 - Salad. Salads.
 - DinnerPlatterName. Contains all possible Dinner Platters names.
 - DinnerPlatter. A model for Dinner Platters items.
 - Order. Represents customers orders (current or closed).
 - OrderPizza, OrderSub, OrderPasta, OrderSalad, OrderDinnerPlatter. These models are "helper" models used for Order model and contain actual order items parameters.
## Files
- orders/static/orders directory contains all static files used in project.
    - js. Directory for JavaScript files.
      - confirm.js A script user in order confirming page.
      - remove.js Contains actions run while removing order items.
      - index.js script for functions specific to index.html and related templates
      - scripts.js Contains all other actions that run throughout the website.
      - orders/templates/orders. A directory to store templates files.
      - base.html. Base HTML template.
      - index.html. Index page template that contains all menu items.
      - login.html. Login page.

      - order.html. A template for showing a single order items.
      - orders_history.html. This template shows all orders page.
      - register.html. A register template.
      --> each food item has a specific html page for its ordering options and is included in rendering index.html
## Personal Touch

All site administrators are able to mark orders as "Completed" through Admin page
A customer can remove items from unsent order before confirm.
