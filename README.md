# Changelog for v1.1

- Provided some basic tests in tests.py
- Simplified the way the JavaScript module handles AJAX requests. There were two similar functions in this area, now there is one.
- Few minor changes here and there (adding/removing spaces here and there, that kind of thing)
- Integrated the repo with Travis CI, added a YML file. Tests are now run automatically with every commit.
- Added a Docker image to the repo. Failed to test as Docker doesn't like something in my BIOS settings. Will have to check that out later.




# cs50w-project3
This is my implementation of the fourth project in the CS50W course. Our tasks in this project were to become more comfortable with using Django and to gain experience in relational database design. In order to achieve this, we needed to design a restaurant website based on Pinocchio's Pizza and Subs (http://www.pinocchiospizza.net/index.html). The project had 7 requirements: 

1. The web application has to support all elements on Pinocchio's menu.
2. Site administrators (members of staff) should be able to edit, add and remove menu elements using Django Admin.
3. Site users (customers) should be able to register, log in and log out of the website.
4. Upon logging in to the site, users should be able to browse the restaurant's menu. They should be able to add items (along with toppings and extras, wherever applicable) to a virtual shopping cart. The contents of their cart should be saved, even if the user closes the window, or logs out of the website.
5. Once there is at least one item in the shopping cart, users should be allowed to place an order.
6. Site administrators should have access to a page where they can view orders that have been placed.
7. Add a "personal touch" to the page. My chosen personal touch is to allow site administrators to mark orders as complete.

Here is a rundown of all the files in the repository that I have modified/created:

- views.py holds all the Django views. As such it is responsible for much of the server's functionality. Most of the views in this file (with the exception of index, register and login_view) only accept POST requests. 
- admin.py connects database models to Django Admin.
- forms.py contains the register and login forms. The rest of the forms used by the app are custom-made. At first, I tried to rely solely on Django's forms (in order to fulfill the goal of becoming more comfortable with using Django), but I failed miserably. I got frustrated so much that I decided to just build the rest of the forms myself.
- helpers.py contains 6 functions that are used in views.py. Three of them rearrange model elements to build the menu for pizzas, subs and dinner platters (one functions for each). Two of them are for organizing data to be used by forms. The last one is for creating shopping cart items according to the users' choices.
- models.py contains all the Django database models.
- urls.py (in the orders folder) connects views to urls.
- scripts.js contains all of the JavaScript used by the application. I used ECMAScript 6 syntax for this project. JavaScript does a few things in this application: it shows the correct prices for the selected pizzas, subs and dinner platters; It checks to see if the user has correctly completed the pizzas form, and notifies them about if something's wrong (regarding the selection of toppings), while barring them from submitting the form before correcting the error; It handles the shopping cart actions (deleting an item from the cart, emptying the cart, placing an order). If the shopping cart is empty, it prevents the user from accessing these functions.
- styles.css contains the custom CSS for the web app. The app's appearance is virtually copied off of the original site. There a few differences due to me adding Bootstrap into the mix.
- db.sqlite3 is the database file containing all the tables.
- urls.py (in the pizza folder) connects the 'orders' apps's urls to the 'pizza' project. This is necessary because of the way Django operates.
- base.html is the HTML template on which all pages are based on.
- index.html is contains the HTML for the main page. This page has the menu, the forms for adding items to the shopping cart, the cart itself and the orders table.
- login.html contains the HTML for the login form.
- register.html contains the HTML for the register form.

