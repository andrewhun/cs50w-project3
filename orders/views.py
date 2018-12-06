import json
from django.urls import reverse
from django.db.models import Sum
from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Pasta, Salad, Topping, Pizza, Platter, Sub, Cart, Order, Extra
from .helpers import organize_pizzas, organize_subs, organize_platters, form_organizer_1, form_organizer_2, shopping_cart



# Create your views here.

def index(request):
	'''Show menu and allow users to select food type to order'''

	if request.method == "GET":
			
		# if the user is not logged in redirect them to the login page
		if not request.user.is_authenticated:
			
			return HttpResponseRedirect(reverse("login"))
		
		else:
			
			# prepare pizzas for the menu
			regular_list = organize_pizzas("Regular")
			sicilian_list = organize_pizzas("Sicilian")

			# prepare subs for the menu
			subs = organize_subs()
			subs["Extra Cheese on any sub"] = ["+0.50", "+0.50"]
			sub_extras = {"+Mushrooms": ["+0.50", "+0.50"], "+Green Peppers": ["+0.50", "+0.50"], 
			"+Onions": ["+0.50", "+0.50"]}

			# prepare dinner platters for the menu
			platter_dict = organize_platters()

			# set up the pizza form 
			pizza_type = form_organizer_1(Pizza, "name")
			pizza_size = form_organizer_1(Pizza, "size")
			pizza_toppings = form_organizer_1(Pizza, "toppings")
			topping_name = form_organizer_1(Topping, "name")

			# set up the subs form
			sub_name = form_organizer_1(Sub, "name")
			sub_size = form_organizer_1(Sub, "size")
			extra_name = form_organizer_1(Extra, "name")

			# set up the pasta form
			pasta_dict = form_organizer_2(Pasta)

			# set up the salads form
			salad_dict = form_organizer_2(Salad)

			#set up the platters form
			platter_name = form_organizer_1(Platter, "name")
			platter_size = form_organizer_1(Platter, "size")

			# set up the shopping cart
			cart = Cart.objects.filter(user = request.user)
			total = cart.aggregate(Sum("price"))["price__sum"]

			#set up the orders list
			orders = Order.objects.filter(user = request.user)

			# set up template variables
			context = {"toppings": Topping.objects.all(),"pastas": Pasta.objects.all(),
			 "salads": Salad.objects.all(), "j": len(platter_dict), "platter_dict": platter_dict, 
			 "regular_list": regular_list, "sicilian_list": sicilian_list, "subs": subs, "sub_extras": sub_extras,
			 "pizza_type": pizza_type, "pizza_size": pizza_size, "pizza_toppings": pizza_toppings,
		 	 "topping_name": topping_name, "cart": cart, "total": total, "orders": orders,
		 	 "sub_name": sub_name, "sub_size": sub_size, "extra_name": extra_name, "pasta_dict": pasta_dict,
		 	 "salad_dict": salad_dict, "platter_name": platter_name, "platter_size": platter_size}
			
			# if the user has logged in show them the main page
			return render(request, "orders/index.html", context = context)
	else:
		return HttpResponse("Error. Wrong request method.")


def pizza_view(request):
	'''Handle Pizza orders'''

	# Show an error if the user reaches the route via GET
	if request.method == "GET":
		
		return HttpResponse("Error. Wrong request method.")

	else:
		# check if the user has decided to add any toppings
		if "topping_name" not in request.POST.keys():
			my_toppings = "no"
		else:
			my_toppings = request.POST.getlist("topping_name")

		# add the selected pizza to the shopping cart
		shopping_cart(request, Pizza, request.POST["pizza_type"], request.POST["pizza_size"], 
			toppings = request.POST["pizza_toppings"], topping_list = my_toppings)

		# reload the page
		return HttpResponseRedirect(reverse("index"))

def pasta_view(request):
	'''Handle Pasta orders'''
	
	# Show an error if the user reaches the route via GET
	if request.method == "GET":

		return HttpResponse("Error. Wrong request method.")

	else:
		# add the selected pasta to the shopping cart
		shopping_cart(request, Pasta, request.POST["pasta_name"])

		# reload the page
		return HttpResponseRedirect(reverse("index"))

def salad_view(request):
	'''Handle Salad orders'''
	
	# Show an error if the user reaches the route via GET
	if request.method == "GET":

		return HttpResponse("Error. Wrong request method.")

	else:
		# add the selected salad to the shopping cart
		shopping_cart(request, Salad, request.POST["salad_name"])
		
		return HttpResponseRedirect(reverse("index"))

def platter_view(request):
	'''Handle Platter orders'''

	# Show an error if the user reaches the route via GET
	if request.method == "GET":

		return HttpResponse("Error. Wrong request method.")

	else:

		# add the selected platter to the shopping cart
		shopping_cart(request, Platter, request.POST["platter_name"], request.POST["platter_size"])

		# reload the page
		return HttpResponseRedirect(reverse("index"))

def sub_view(request):
	'''Handle Sub orders'''

	# Show an error if the user reaches the route via GET
	if request.method == "GET":

		return HttpResponse("Error. Wrong request method.")

	else:

		# check if the user wanted extra cheese
		if "extra_cheese" not in request.POST.keys():
			cheese = "no"
		else:
			cheese = request.POST["extra_cheese"]
		
		# check if the user wanted any other extras, then add the selected sub to the shopping cart
		if "extra_name" in request.POST.keys():
		
			shopping_cart(request, Sub, request.POST["sub_name"], request.POST["sub_size"],
				extras = request.POST.getlist("extra_name"), cheese = cheese)
		
		else:
			
			shopping_cart(request, Sub, request.POST["sub_name"], request.POST["sub_size"],
				extras = "no", cheese = cheese)
		
		# reload the page
		return HttpResponseRedirect(reverse("index"))

def cart_view(request):
	'''Allow users to interact with their shopping cart'''
	
	# Show an error if the user reaches the route via GET
	if request.method == "GET":

		return HttpResponse("Error. Wrong request method.")
	
	else:

		# delete the selected cart element
		if request.POST["post_type"] == "delete":

			c = Cart.objects.get(id = request.POST["my_id"])

			print(c)
			c.delete()

			return HttpResponseRedirect(reverse("cart"))
		
		# empty the shopping cart
		elif request.POST["post_type"] == "empty":

			c = Cart.objects.filter(user = request.user)
			c.delete()

			return HttpResponseRedirect(reverse("cart"))

		# place an order
		else:
			# create a new order object, using the titles of the shopping cart elements
			# and the sum of their prices
			cart = Cart.objects.filter(user = request.user)
			total = cart.aggregate(Sum("price"))["price__sum"]
			my_order = ""
			for my_object in cart:
				my_order = f"{my_order} {my_object.title},"

			o = Order(user = request.user, title = my_order, price = total)
			o.save()

			# empty the cart once the order is placed
			cart.delete()

			# reload the page
			return HttpResponseRedirect(reverse("index"))
		

# This is now redundant.
def order_view(request):
	''' Handle customer orders '''

	orders = Order.objects.filter(user = request.user)

	return render(request, "orders/orders-page.html", {"orders": orders})


def price_view(request):
	''' Return the price of the currently selected meal '''

	if request.method == "POST":

		# grab the food type (pizza, sub or platter)
		food_type = request.POST["food_type"]

		# find the price of the selected pizza
		if food_type == "pizzas":
			
			price = Pizza.objects.values_list("price").filter(name = request.POST["pizza_type"], 
				size = request.POST["pizza_size"], toppings = request.POST["pizza_toppings"])

			price = price[0]

		# find the price of the selected sub
		elif food_type == "subs":

			price = Sub.objects.values_list("price").filter(name = request.POST["sub_name"],
				size = request.POST["sub_size"])

			price = float(price[0][0])

			# increase the price according to the menu if the user wants any extras
			price += (int(request.POST["sub_extras"]) * 0.50)

			if request.POST["extra_cheese"] == "yes":

				price += 0.50

		# find the price of the selected platter
		else:

			price = Platter.objects.values_list("price").filter(name = request.POST["platter_name"],
				size = request.POST["platter_size"])

			price = price[0]

		# return the price
		return HttpResponse(price)
	
	else:
		# Return an error if the user reached the route via GET
		return HttpResponse("Error. Wrong request method.")


def login_view(request):
	''' Log users in'''

	# the user reached the route via POST
	if request.method == "POST":

		# grab the user input and place it in variables
		username = request.POST["login_user"]
		password = request.POST["login_pw"]

		# authenticate the user
		user = authenticate(request, username=username, password=password)

		# log the user in and redirect them to the main page if they were successfully authenticated
		
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		
		# if the authentication failed reload the login page and show an error message
		else:
			return render(request, "orders/login.html", {"form": LoginForm(), "message": "Invalid credentials!"})
	
	# the user reached the route via GET
	else:
		
		# render the login page		
		form = LoginForm()
		return render(request, "orders/login.html", {"form": form})

def register(request):
	'''Register users'''
	
	# the user reached the route via POST
	if request.method == "POST":
		
		# check the database to see if the username is in use
		my_user = User.objects.filter(username = request.POST["reg_user"])
		
		if len(my_user) != 0:
			
			# username was taken, reload the page with an error message
			return render(request, "orders/register.html", {"message": "Username already taken!", "form": RegisterForm()})
		
		# password mismatch
		elif request.POST["reg_pw"] != request.POST["reg_conf"]:
			return render(request, "orders/register.html", {"message": "Password and its confirmation do not match!", 
				"form": RegisterForm()})
		
		# success
		else:

			# add user to the database
			user = User.objects.create_user(username = request.POST["reg_user"], email = request.POST["reg_email"],
			first_name = request.POST["reg_firstname"], last_name = request.POST["reg_lastname"], 
			password = request.POST["reg_pw"],)
			user.save()

		# redirect user to the main page
		return HttpResponseRedirect(reverse("index"))
	
	# user reached the route via GET
	else:

		# render the page
		form = RegisterForm()
		return render(request, "orders/register.html", {"form": form})

def logout_view(request):
	'''Log users out.'''
	
	logout(request)

	# redirect user to the login page
	return HttpResponseRedirect(reverse("login"))
