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

def create_title_from_pizza(pizza, topping_list):

	# format the name according to what the user has selected
	if pizza.toppings == 0:
		
		# no toppings means its a pizza with cheese
		title = f"{pizza} pizza with cheese"
	else:

		# let users know what toppings are on their pizza
		my_topping = ""
		for topping in topping_list:
			my_topping = f"{my_topping} {topping},"
		title = f"{pizza} pizza with {pizza.toppings} topping(s):{my_topping}"
	
	return title

def create_title_from_platter(platter):
	''' Create a shopping cart title from a dinner platter object. '''

	title = f"{platter} dinner platter"

	return title

def create_title_from_sub(sub, extras, cheese):

	''' Create a shopping cart title from a sub object. '''

	title = f"{sub} sub"

	if extras != "no":

		# let the user know what extras are added to the sub
		my_extras = ""
		for extra in extras:
			my_extras = f"{my_extras} {extra},"
		
		title = f"{title} with {len(extras)} extra(s):{my_extras}"

	# let the user know if extra cheese has been added to the sub
	if cheese == "yes":

		title = f"{title} with extra cheese"

	return title

def create_title_from_pasta(pasta):
	''' Create a shopping cart title from a pasta object. '''

	title = f"{pasta} pasta"

	return title

def create_title_from_salad(salad):
	''' Create a shopping cart title from a salad object. '''

	if salad.name == "Antipasto":
		title = f"{salad} salad"
	else:
		title = f"{salad}"

	return title

def calculate_sub_price(sub, extras, cheese):
	''' Calculate the final price of the selected sub variation. '''

	price = float(sub.price)

	if extras != "no":

		price += len(extras) * 0.50

	if cheese == "yes":

		price += 0.50

	return price

def create_cart_object(user, title, price):
	''' Create a shopping cart object '''

	c = Cart(user = user, title = title, price = price)
	
	c.save()

def get_current_user(request):
	''' Find the user associated with the current request. '''

	current_user = User.objects.get(username = request.user)

	return current_user