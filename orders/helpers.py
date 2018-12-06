from django.contrib.auth.models import User
from .models import Pizza, Sub, Platter, Pasta, Cart, Salad

def organize_pizzas(my_type):
	''' Arrange information regarding pizzas in a list that can be used to create the menu '''
	
	# grab all topping values from the Pizza model (0, 1, 2, 3, 4)
	toppings = Pizza.objects.values_list("toppings").distinct()
	my_list = []
	
	# iterate through the list of toppings
	for topping in toppings:
		
		# add each of them to the newly created list
		my_list.append([topping[0]])
		
		# grab the two prices (small, large) belonging to each topping
		prices = Pizza.objects.values_list("price").filter(name = my_type, toppings = topping[0])
		
		# add both prices to the earlier list, creating a list of lists in the process
		for price in prices:
			
			# this syntax is tricky; it takes advantage of the fact that the number of toppings are
			# basically zero-indexed, which makes them perfect for list-indexing
			my_list[topping[0]].append(price[0])

	# format each element in the list created earlier to match the look of the example menu
	for element in my_list:

		if element[0] == 0:
			element[0] = "Cheese"

		elif element[0] == 1:
			element[0] = str(element[0]) + " Topping"

		else:
			element[0] = str(element[0]) + " Toppings"

	# return the list
	return my_list

def organize_subs():
	''' Arrange information regarding subs in a list that can be used to create the menu '''
	
	# grab all the different sub names
	names = Sub.objects.values_list("name").distinct()
	my_dict = {}

	# iterate through the list of names
	for name in names:

		# grab the two prices (small, large) belonging to each name
		prices = Sub.objects.values_list("price").filter(name = name[0])
		
		# this particular sub is only available in large size
		if name[0] == "Sausage, Peppers & Onions":
			
			# create a dictionary where the names are the keys 
			# and the values are a list of prices that belong to them
			my_dict[name[0]] = ["", prices[0][0]]
		else:
			my_dict[name[0]] = [prices[0][0], prices[1][0]]

	# return the dictionary
	return my_dict

def organize_platters():
	''' Arrange information regarding dinner platters in a list that can be used to create the menu '''
	
	# grab all the different platter names
	names = Platter.objects.values_list("name").distinct()
	my_dict = {}

	# iterate through the list of names
	for name in names:

		# grab the two prices (small, large) belonging to each name
		prices = Platter.objects.values_list("price").filter(name = name[0])

		# create a dictionary where the names are the keys
		# and the values are a list of prices that belong to them
		my_dict[name[0]] = [prices[0][0], prices[1][0]]

	# return the dictionary
	return my_dict

def form_organizer_1(Food, attribute):
	''' Rearrange model elements to make them usable for HTML forms '''

	# grab a list of all the different "attributes" the user has selected from the food type
	# of the user's choosing
	foods = Food.objects.values_list(attribute).distinct()
	food_type = []
	
	# format the list (get the values out of the tuples Django presents them in)
	for stuff in foods:
		food_type.append(stuff[0])

	# return the list
	return food_type

def form_organizer_2(Food):
	''' Rearrange model elements to make them usable for HTML forms. A slightly different variation. '''

	# grab all instances of the selected model
	foods = Food.objects.all()
	food_dict = {}
	# create a dictionary where the names are the keys and their prices are the values
	for food in foods:
		food_dict[food.name] = food.price

	# return the dictionary
	return food_dict

def shopping_cart(request, Food, name, size = "", toppings = "", extras = "", cheese = "", topping_list = ""):
	''' Add selected foods to the user's shopping cart '''
	
	# the user wants to add a dinner platter to the shopping cart
	if size and not (toppings or extras):

		# grab the selected platter and its price
		food = Food.objects.get(name = name, size = size)
		price = food.price
		
		# format the name properly so the user can tell what's in their cart
		food = f"{food} dinner platter"
		
	# the user wants to add a pizza to the shopping cart
	elif size and toppings:
		
		# grab the selected pizza and its price
		food = Food.objects.get(name = name, size = size, toppings = toppings)
		price = food.price
		
		# format the name according to what the user has selected
		if toppings == "0":
			# no toppings means its a pizza with cheese
			food = f"{food} pizza with cheese"
		else:

			# let users know what toppings are on their pizza
			my_topping = ""
			for topping in topping_list:
				my_topping = f"{my_topping} {topping},"
			food = f"{food} pizza with {toppings} topping(s):{my_topping}"
		
	# the user wants to add a sub to the shopping cart
	elif size and extras:
		
		# grab the selected sub and its price
		food = Food.objects.get(name = name, size = size)
		price = food.price
		price = float(price)
		# let the user know the item is a sub
		food = f"{food} sub"
		
		# the user wants to add extras to their sub
		if extras != "no":

			# adjust the price of the sub
			price += len(extras) * 0.50

			# let the user know what extras are added to the sub
			my_extras = ""
			for extra in extras:
				my_extras = f"{my_extras} {extra},"
			
			food = f"{food} with {len(extras)} extra(s):{my_extras}"
		
		# the user wants extra cheese
		if cheese == "yes":
			
			# let the user know this sub is with extra cheese
			food = f"{food} with extra cheese"

			# adjust the price of the sub
			price += 0.50

	# the user wants a salad or a pasta
	else:
		# grab the food and its price
		food = Food.objects.get(name = name)
		price = food.price

		# let the user know what food they've got in their cart
		if Food == Pasta:
			food = f"{food} pasta"
		elif Food == Salad and name == "Antipasto":
			food = f"{food} salad"

	# create a new cart object and add it to the database
	my_user = User.objects.get(username = request.user)
	c = Cart(user = my_user, title = food, price = price)
	c.save()