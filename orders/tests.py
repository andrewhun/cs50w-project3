from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase, Client, SimpleTestCase
from orders.views import price_view, login_view, register, logout_view
from orders.models import Pasta, Salad, Topping, Pizza, Platter, Sub, Cart, Order, Extra
from orders.views import index, pizza_view, pasta_view, salad_view, platter_view, sub_view, cart_view, order_view


# Create your tests here.

class RegisterCase(TestCase):
	''' Test the Register url and view. '''

	def setUp(self):
		
		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", 
			password = "testpass1",)
		
		User.objects.create_user(username = "test2", email = "test2@test.com",
			first_name = "Tester", last_name = "Testerson", 
			password = "testpass2",)

	def test_register_url(self):

		self.assertEqual(resolve(reverse("register")).func, register)

	def test_register_get(self):

		c = Client()

		response = c.get(reverse('register'))

		self.assertEqual(response.status_code, 200)

	def test_register_username_taken(self):

		c = Client()

		error_message = "Username already taken!"

		response = c.post(reverse('register'), {'reg_user': 'test1', 'reg_pw': 'testpass1', 'reg_conf': 'testpass1', 
			'reg_email': 'test1@test.com', 'reg_firstname': 'Testy', 'reg_lastname': 'McTestyFace'})



		self.assertEqual(response.status_code, 200)
		self.assertIn(error_message, str(response.content))


	def test_register_password_mismatch(self):

		c = Client()

		error_message = "Password and its confirmation do not match!"

		response = c.post(reverse('register'), {'reg_user': 'test3', 'reg_pw': 'testpass3','reg_conf': 'asd', 
			'reg_email': 'test3@test.com','reg_firstname': 'Test', 'reg_lastname': 'Successful'})

		self.assertEqual(response.status_code, 200)
		self.assertIn(error_message, str(response.content))

	def test_register_valid_input(self):

		c = Client()

		response = c.post(reverse('register'), {'reg_user': 'test3', 'reg_pw': 'testpass3','reg_conf': 'testpass3', 
			'reg_email': 'test3@test.com','reg_firstname': 'Test', 'reg_lastname': 'Successful'})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/')
		self.assertEqual(len(User.objects.all()), 3)

class LoginCase(TestCase):
''' Test the Login url and view. '''

	def setUp(self):
		
		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", 
			password = "testpass1",)
		
		User.objects.create_user(username = "test2", email = "test2@test.com",
			first_name = "Tester", last_name = "Testerson", 
			password = "testpass2",)

	def test_login_url(self):

		self.assertEqual(resolve(reverse("login")).func, login_view)

	def test_login_get(self):

		c = Client()

		response = c.get(reverse('login'))

		self.assertEqual(response.status_code, 200)

	def test_invalid_input(self):

		c = Client()

		response = c.post(reverse('login'), {'login_user': 'test3', 'login_pw': 'testpass3'})

		self.assertEqual(response.status_code, 200)
		self.assertIn("Invalid credentials!", str(response.content))
		self.assertFalse(authenticate(username = 'test3', password = 'testpass3'))

	def test_login_valid_input(self):

		c = Client()

		response = c.post(reverse('login'), {'login_user': 'test2', 'login_pw': 'testpass2'})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/")
		self.assertTrue(authenticate(username = 'test2', password = 'testpass2'))

class LogoutCase(TestCase):
	''' Test the Logout url and view. '''

	def setUp(self):

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", 
			password = "testpass1",)

	def test_logout_url(self):

		self.assertEqual(resolve(reverse("logout")).func, logout_view)

	def test_logout(self):

		c = Client()

		c.login(username = 'test1', password = 'testpass1')

		response = c.get(reverse('logout'))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/login/")

		second_response = c.get(reverse("index"))

		self.assertEqual(second_response.status_code, 302)
		self.assertEqual(second_response.url, "/login/")

class IndexCase(TestCase):
	''' Test the main page and the index view '''
	def setUp(self):

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", 
			password = "testpass1",)

		user = User.objects.get(username = "test1")

		Cart.objects.create(user = user, title = "Baked Ziti pasta", price = 6.50)
		Order.objects.create(user = user, title = "Antipasto salad, Small Sicilian pizza,", price = 42.20,
		 status = "Pending")

	def test_index_url(self):

		self.assertEqual(resolve(reverse("index")).func, index)

	def test_index_view(self):

		c = Client()

		post_response = c.post(reverse("index"))

		self.assertIn("Error. Wrong request method.", str(post_response.content))

		response = c.get(reverse("index"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/login/")

		c.login(username = "test1", password = "testpass1")

		response2 = c.get(reverse("index"))

		self.assertEqual(response2.status_code, 200)

		self.assertIn("Our Menu</h2>", str(response2.content))
		self.assertIn("Order it here!</h2>", str(response2.content))
		self.assertIn("Shopping Cart</th>", str(response2.content))
		self.assertIn("Orders</th>", str(response2.content))

		


class PizzaCase(TestCase):
''' Test the Pizza model, url, menu, form, view and price. Test the Topping model. '''

	def setUp(self):

		Topping.objects.create(name = "Salami")
		Topping.objects.create(name = "Chillies")

		Pizza.objects.create(name = "Sicilian", toppings = 0, size = "Small", price = 23.45)
		Pizza.objects.create(name = "Sicilian", toppings = 0, size = "Large", price = 37.70)
		Pizza.objects.create(name = "Regular", toppings = 1, size = "Small", price = 13.20)
		Pizza.objects.create(name = "Regular", toppings = 1, size = "Large", price = 19.45)
		Pizza.objects.create(name = "Regular", toppings = 2, size = "Small", price = 14.70)
		Pizza.objects.create(name = "Regular", toppings = 2, size = "Large", price = 21.45)

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", password = "testpass1",)

	def test_pizza_model(self):

		pizza = Pizza(name = "Regular", toppings = 4, size = "Large", price = 24.40)

		pizza.save()

		pizza2 = Pizza.objects.get(name = "Sicilian", size = "Small")

		self.assertEqual(len(Pizza.objects.all()), 7)
		self.assertEqual(str(pizza), "Large Regular")
		self.assertEqual(str(pizza2), "Small Sicilian")

	def test_topping_model(self):

		topping = Topping(name = "Anchovies")
		topping.save()

		topping2 = Topping.objects.get(name = "Salami")

		self.assertEqual(len(Topping.objects.all()), 3)
		self.assertEqual(str(topping), "Anchovies")
		self.assertEqual(str(topping2), "Salami")

	def test_pizza_url(self):

		self.assertEqual(resolve(reverse("pizzas")).func, pizza_view)

	def test_pizza_menu(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Regular Pizza</th>", str(response.content))
		self.assertIn("<td>Small</td>", str(response.content))
		self.assertIn("<td>Large</td>", str(response.content))
		self.assertIn("<td>1 Topping</td>", str(response.content))
		self.assertIn("<td>13.20</td>", str(response.content))
		self.assertIn("<td>19.45</td>", str(response.content))
		self.assertIn("<td>2 Toppings</td>", str(response.content))

		self.assertIn("Sicilian Pizza</th>", str(response.content))
		self.assertIn("<td>Small</td>", str(response.content))
		self.assertIn("<td>Large</td>", str(response.content))
		self.assertIn("<td>Cheese</td>", str(response.content))
		self.assertIn("<td>23.45</td>", str(response.content))
		self.assertIn("<td>37.70</td>", str(response.content))

		self.assertIn("Toppings</th>", str(response.content))
		self.assertIn("<td>Salami</td>", str(response.content))
		self.assertIn("<td>Chillies</td>", str(response.content))

	def test_pizza_form(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Pizzas</h3>", str(response.content))

		self.assertIn("Regular</option>", str(response.content))
		self.assertIn("Sicilian</option>", str(response.content))

		self.assertIn("Small</option>", str(response.content))
		self.assertIn("Large</option>", str(response.content))

		self.assertIn("0</option>", str(response.content))
		self.assertIn("1</option>", str(response.content))
		self.assertIn("2</option>", str(response.content))

		self.assertIn("Salami</option>", str(response.content))
		self.assertIn("Chillies</option>", str(response.content))

	def test_pizza_view(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("pizzas"))

		self.assertIn("Error. Wrong request method.", str(response.content))

		response2 = c.post(reverse("pizzas"), {"pizza_type": "Regular", "pizza_size": "Large", 
			"pizza_toppings": 2, "topping_name": ["Salami", "Chillies"]})

		cart = Cart.objects.get(price = 21.45)

		self.assertEqual(len(Cart.objects.all()), 1)
		self.assertEqual(str(cart), "test1: Large Regular pizza with 2 topping(s): Salami, Chillies, for 21.45")

		response3 = c.post(reverse("pizzas"), {"pizza_type": "Sicilian", "pizza_size": "Small", 
			"pizza_toppings": 0})

		cart2 = Cart.objects.get(price = 23.45)

		self.assertEqual(len(Cart.objects.all()), 2)
		self.assertEqual(str(cart2), "test1: Small Sicilian pizza with cheese for 23.45")

	def test_pizza_price(self):

		self.assertEqual(resolve(reverse("price")).func, price_view)

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("price"))

		self.assertIn("Error. Wrong request method.", str(response.content))

		response2 = c.post(reverse("price"), {"food_type": "pizzas", "pizza_type": "Sicilian",
			"pizza_size": "Large", "pizza_toppings": 0})

		self.assertEqual("b'37.70'", str(response2.content))

class SubCase(TestCase):
	''' Test the Sub model, url, menu, form, view and price.  Test the Extra model.'''
	def setUp(self):

		Sub.objects.create(name = "Cheese", size = "Small", price = 6.50)
		Sub.objects.create(name = "Cheese", size = "Large", price = 7.95)
		Sub.objects.create(name = "Sausage, Peppers & Onions", size = "Large", price = 8.50)

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", password = "testpass1",)

		Extra.objects.create(name = "Mushrooms")
		Extra.objects.create(name = "Onions")

	def test_sub_model(self):

		sub = Sub(name = "Italian", size = "Large", price = 8.95)
		sub.save()

		sub2 = Sub.objects.get(name = "Cheese", size = "Small")

		self.assertEqual(len(Sub.objects.all()), 4)
		self.assertEqual(str(sub), "Large Italian")
		self.assertEqual(str(sub2), "Small Cheese")

	def test_extra_model(self):

		extra = Extra(name = "Green Peppers")
		extra.save()

		extra2 = Extra.objects.get(name = "Mushrooms")

		self.assertEqual(len(Extra.objects.all()), 3)
		self.assertEqual(str(extra), "Green Peppers")
		self.assertEqual(str(extra2), "Mushrooms")

	def test_sub_url(self):

		self.assertEqual(resolve(reverse("subs")).func, sub_view)

	def test_sub_menu(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Subs</th>", str(response.content))
		self.assertIn("<td>Small</td>", str(response.content))
		self.assertIn("<td>Large</td>", str(response.content))
		self.assertIn("<td>Cheese</td>", str(response.content))
		self.assertIn("<td>6.50</td>", str(response.content))
		self.assertIn("<td>7.95</td>", str(response.content))
		self.assertIn("<td>Sausage, Peppers &amp; Onions</td>", str(response.content))
		self.assertIn("<td></td>", str(response.content))
		self.assertIn("<td>Extra Cheese on any sub</td>", str(response.content))
		self.assertIn("<td>+0.50</td>", str(response.content))

		Sub.objects.create(name = "Steak + Cheese", size = "Small", price = 6.95)
		Sub.objects.create(name = "Steak + Cheese", size = "Large", price = 8.50)

		response = c.get(reverse("index"))

		self.assertIn("<td>Steak + Cheese</td>", str(response.content))
		self.assertIn("<td>6.95</td>", str(response.content))
		self.assertIn("<td>8.50</td>", str(response.content))
		self.assertIn("<td>+Mushrooms</td>", str(response.content))
		self.assertIn("<td>+Onions</td>", str(response.content))

	def test_sub_form(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Subs</h3>", str(response.content))

		self.assertIn("Small</option>", str(response.content))
		self.assertIn("Large</option>", str(response.content))

		self.assertIn("Cheese</option>", str(response.content))
		self.assertIn("Sausage, Peppers &amp; Onions</option>", str(response.content))

		self.assertIn("Mushrooms</option>", str(response.content))
		self.assertIn("Onions</option>", str(response.content))

		self.assertIn('<input type = "checkbox"', str(response.content))

	def test_sub_view(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("subs"))

		self.assertIn("Error. Wrong request method.", str(response.content))

		response2 = c.post(reverse("subs"), {"sub_name": "Cheese", "sub_size": "Small"})

		cart = Cart.objects.get(price = 6.50)

		self.assertEqual(len(Cart.objects.all()), 1)
		self.assertEqual(str(cart), "test1: Small Cheese sub for 6.50")

		Sub.objects.create(name = "Steak + Cheese", size = "Small", price = 6.95)
		Sub.objects.create(name = "Steak + Cheese", size = "Large", price = 8.50)

		response3 = c.post(reverse("subs"), {"sub_name": "Steak + Cheese", "sub_size": "Large",
			"extra_name": ["Mushrooms", "Onions"]})

		cart2 = Cart.objects.get(price = 9.50)

		self.assertEqual(len(Cart.objects.all()), 2)
		self.assertEqual(str(cart2), "test1: Large Steak + Cheese sub with 2 extra(s): Mushrooms, Onions, for 9.50")

		response4 = c.post(reverse("subs"), {"sub_name": "Sausage, Peppers & Onions", "sub_size": "Large",
			"extra_cheese": "yes"})

		cart3 = Cart.objects.get(price = 9.00)

		self.assertEqual(len(Cart.objects.all()), 3)
		self.assertEqual(str(cart3), "test1: Large Sausage, Peppers & Onions sub with extra cheese for 9.00")

		response5 = c.post(reverse("subs"), {"sub_name": "Steak + Cheese", "sub_size": "Small",
			"extra_cheese": "yes", "extra_name": ["Mushrooms", "Onions"]})

		cart4 = Cart.objects.get(price = 8.45)

		self.assertEqual(len(Cart.objects.all()), 4)
		self.assertEqual(str(cart4), 
			"test1: Small Steak + Cheese sub with 2 extra(s): Mushrooms, Onions, with extra cheese for 8.45")


	def test_sub_price(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.post(reverse("price"), {"food_type": "subs", "sub_name": "Cheese", "sub_size": "Small",
			"sub_extras": 0, "extra_cheese": "no"})

		self.assertEqual("b'6.5'", str(response.content))

		response2 = c.post(reverse("price"), {"food_type": "subs", "sub_name": "Sausage, Peppers & Onions",
			"sub_size": "Large", "sub_extras": 2, "extra_cheese": "yes"})

		self.assertEqual("b'10.0'", str(response2.content))

class PastaCase(TestCase):
	''' Test the Pasta model, url, menu, form and view. '''

	def setUp(self):

		Pasta.objects.create(name = "Baked Ziti", price = 6.50)

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", password = "testpass1",)

	def test_pasta_model(self):

		pasta = Pasta(name = "Bolognese", price = 8.00)
		pasta.save()

		pasta2 = Pasta.objects.get(name = "Baked Ziti")

		self.assertEqual(len(Pasta.objects.all()), 2)
		self.assertEqual(str(pasta), "Bolognese")
		self.assertEqual(str(pasta2), "Baked Ziti")

	def test_pasta_url(self):

		self.assertEqual(resolve(reverse("pasta")).func, pasta_view)

	def test_pasta_menu(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Pasta</th>", str(response.content))
		self.assertIn("<td>Baked Ziti</td>", str(response.content))
		self.assertIn("<td>6.50</td>", str(response.content))

	def test_pasta_form(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Pasta</h3>", str(response.content))
		self.assertIn("Baked Ziti (6.50)</option>", str(response.content))

	def test_pasta_view(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("pasta"))

		self.assertIn("Error. Wrong request method.", str(response.content))

		response2 = c.post(reverse("pasta"), {"pasta_name": "Baked Ziti"})

		cart = Cart.objects.get(price = 6.50)

		self.assertEqual(len(Cart.objects.all()), 1)
		self.assertEqual(str(cart), "test1: Baked Ziti pasta for 6.50")

class SaladCase(TestCase):
	''' Test the Salad model, url, menu, form, view and price. '''

	def setUp(self):

		Salad.objects.create(name = "Antipasto", price = 8.25)

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", password = "testpass1",)

	def test_salad_model(self):

		salad = Salad(name = "Greek Salad", price = 7.65)
		salad.save()

		salad2 = Salad.objects.get(name = "Antipasto")

		self.assertEqual(len(Salad.objects.all()), 2)
		self.assertEqual(str(salad), "Greek Salad")
		self.assertEqual(str(salad2), "Antipasto")

	def test_salad_url(self):

		self.assertEqual(resolve(reverse("salads")).func, salad_view)

	def test_salad_menu(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Salads</th>", str(response.content))
		self.assertIn("<td>Antipasto</td>", str(response.content))
		self.assertIn("<td>8.25</td>", str(response.content))

	def test_salad_form(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Salads</h3>", str(response.content))
		self.assertIn("Antipasto (8.25)</option>", str(response.content))

	def test_salad_view(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("salads"))

		self.assertIn("Error. Wrong request method.", str(response.content))

		response2 = c.post(reverse("salads"), {"salad_name": "Antipasto"})

		cart = Cart.objects.get(price = 8.25)

		self.assertEqual(len(Cart.objects.all()), 1)
		self.assertEqual(str(cart), "test1: Antipasto salad for 8.25")

class PlatterCase(TestCase):
	''' Test the Dinner Platter model, url, menu, form, view and price. '''
	def setUp(self):

		Platter.objects.create(name = "Garden Salad", size = "Small", price = 35.00)
		Platter.objects.create(name = "Garden Salad", size = "Large", price = 60.00)

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", password = "testpass1",)

	def test_platter_model(self):

		platter = Platter(name = "Chicken Parm", size = "Large", price = 80.00)
		platter.save()

		platter2 = Platter.objects.get(name = "Garden Salad", size = "Small")

		self.assertEqual(len(Platter.objects.all()), 3)
		self.assertEqual(str(platter), "Large Chicken Parm")
		self.assertEqual(str(platter2), "Small Garden Salad")

	def test_platter_url(self):

		self.assertEqual(resolve(reverse("dinner_platters")).func, platter_view)

	def test_platter_menu(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Dinner Platters</th>", str(response.content))

		self.assertIn("<td>Small</td>", str(response.content))
		self.assertIn("<td>Large</td>", str(response.content))

		self.assertIn("<td>Garden Salad</td>", str(response.content))

		self.assertIn("<td>35.00</td>", str(response.content))
		self.assertIn("<td>60.00</td>", str(response.content))

	def test_platter_form(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Dinner Platters</h3>", str(response.content))

		self.assertIn("Small</option>", str(response.content))
		self.assertIn("Large</option>", str(response.content))

		self.assertIn("Garden Salad</option>", str(response.content))

	def test_platter_view(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("dinner_platters"))

		self.assertIn("Error. Wrong request method.", str(response.content))

		response2 = c.post(reverse("dinner_platters"), {"platter_name": "Garden Salad", "platter_size": "Small"})

		cart = Cart.objects.get(price = 35.00)

		self.assertEqual(len(Cart.objects.all()), 1)
		self.assertEqual(str(cart), "test1: Small Garden Salad dinner platter for 35.00")

	def test_platter_price(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.post(reverse("price"), 
			{"food_type": "platters", "platter_name": "Garden Salad", "platter_size": "Large"})

		self.assertEqual("b'60.00'", str(response.content))

class CartCase(TestCase):
	''' Test the Shopping Cart model, url, table, and view. '''

	def setUp(self):

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", 
			password = "testpass1",)

		user = User.objects.get(username = "test1")

		Cart.objects.create(user = user, title = "Baked Ziti pasta", price = 6.50)

	def test_cart_model(self):

		user = User.objects.get(username = "test1")

		cart = Cart(user = user, title = "Large Chicken Parm dinner platter", price = 80.00)
		cart.save()

		cart2 = Cart.objects.get(price = 6.50)

		self.assertEqual(len(Cart.objects.all()), 2)
		self.assertEqual(str(cart), "test1: Large Chicken Parm dinner platter for 80.0")
		self.assertEqual(str(cart2), "test1: Baked Ziti pasta for 6.50")

	def test_cart_url(self):

		self.assertEqual(resolve(reverse("cart")).func, cart_view)

	def test_cart_table(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Shopping Cart</th>", str(response.content))

		self.assertIn("<th>Title</th>", str(response.content))
		self.assertIn("<th>Price</th>", str(response.content))

		self.assertIn("<td>Baked Ziti pasta</td>", str(response.content))
		self.assertIn("<td>6.50</td>", str(response.content))
		self.assertIn("Total:</td>", str(response.content))

	def test_cart_view(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("cart"))

		self.assertIn("Error. Wrong request method.", str(response.content))

		response2 = c.post(reverse("cart"), {"post_type": "delete", "my_id": 1})

		self.assertEqual(len(Cart.objects.all()), 0)

		user = User.objects.get(username = "test1")

		Cart.objects.create(user = user, title = "Small Garden Salad dinner platter", price = 35.00)
		Cart.objects.create(user = user, title = "Large Sicilian pizza with cheese", price = 37.70)

		self.assertEqual(len(Cart.objects.all()), 2)

		response3 = c.post(reverse("cart"), {"post_type": "empty"})

		self.assertEqual(len(Cart.objects.all()), 0)

		Cart.objects.create(user = user, title = "Small Garden Salad dinner platter", price = 35.00)
		Cart.objects.create(user = user, title = "Large Sicilian pizza with cheese", price = 37.70)

		response4 = c.post(reverse("cart"), {"post_type": "place_order"})

		order = Order.objects.get(price = 72.70)

		self.assertEqual(len(Cart.objects.all()), 0)
		self.assertEqual(len(Order.objects.all()), 1)
		self.assertEqual(str(order), 
			"test1:  Small Garden Salad dinner platter, Large Sicilian pizza with cheese, for 72.70")

class OrderCase(TestCase):
	''' Test the Order model, url, table, and view. '''

	def setUp(self):

		User.objects.create_user(username = "test1", email = "test1@test.com",
			first_name = "Testy", last_name = "McTestyFace", 
			password = "testpass1",)

		user = User.objects.get(username = "test1")

		Order.objects.create(user = user, title = "Antipasto salad, Small Sicilian pizza,", price = 42.20,
		 status = "Pending")

	def test_order_model(self):

		user = User.objects.get(username = "test1")

		order = Order(user = user, title = "Small Chicken Parm dinner platter,", price = 45.00, status = "Pending")
		order.save()

		order2 = Order.objects.get(title = "Antipasto salad, Small Sicilian pizza,")

		self.assertEqual(len(Order.objects.all()), 2)
		self.assertEqual(str(order), "test1: Small Chicken Parm dinner platter, for 45.0")
		self.assertEqual(str(order2), "test1: Antipasto salad, Small Sicilian pizza, for 42.20")

	def test_order_url(self):

		self.assertEqual(resolve(reverse("orders-page")).func, order_view)

	def test_order_table(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		response = c.get(reverse("index"))

		self.assertIn("Orders</th>", str(response.content))

		self.assertIn("<th>Title</th>", str(response.content))
		self.assertIn("<th>Price</th>", str(response.content))
		self.assertIn("<th>Status</th>", str(response.content))

		self.assertIn("<td>Antipasto salad, Small Sicilian pizza,</td>", str(response.content))
		self.assertIn("<td>42.20</td>", str(response.content))
		self.assertIn("<td>Pending</td>", str(response.content))


	def test_order_view(self):

		c = Client()

		c.login(username = "test1", password = "testpass1")

		User.objects.create_user(username = "test2", email = "test2@test.com",
			first_name = "Tester", last_name = "Testerson", 
			password = "testpass2",)

		user = User.objects.get(username = "test2")

		Order.objects.create(user = user, title = "Large Sicilian pizza with cheese,", price = 37.70, status = "Pending")

		response = c.get(reverse("orders-page"))

		self.assertEqual(len(Order.objects.all()), 2)
		self.assertNotIn("<td>Large Sicilian pizza with cheese,</td>", str(response.content))
		self.assertNotIn("<td>37.70</td>", str(response.content))