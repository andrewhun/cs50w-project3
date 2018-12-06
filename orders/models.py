from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pasta(models.Model):
	

	name = models.CharField(max_length = 50)
	price = models.DecimalField(max_digits = 3, decimal_places = 2)

	def __str__(self):
		return self.name

class Salad(models.Model):
	
	name = models.CharField(max_length = 50)
	price= models.DecimalField(max_digits = 4, decimal_places = 2)

	def __str__(self):
		return self.name

class Topping(models.Model):

	name = models.CharField(max_length = 50)

	def __str__(self):
		return self.name

class Pizza(models.Model):
	

	name = models.CharField(max_length = 50)
	toppings = models.IntegerField()
	size = models.CharField(max_length = 50)
	price = models.DecimalField(max_digits = 4, decimal_places = 2)

	def __str__(self):
		return f"{self.size} {self.name}"

class Platter(models.Model):

	name = models.CharField(max_length = 50)
	size = models.CharField(max_length = 50)
	price = models.DecimalField(max_digits = 4, decimal_places = 2)

	def __str__(self):
		return f"{self.size} {self.name}"

class Sub(models.Model):
	
	name = models.CharField(max_length = 50)
	size = models.CharField(max_length = 50)
	price = models.DecimalField(max_digits = 3, decimal_places = 2)

	def __str__(self):
		return f"{self.size} {self.name}"

class Cart(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits = 6, decimal_places = 2)

	def __str__(self):
		return f"{self.user}: {self.title} for {self.price}"

class Order(models.Model):

	status_choices = (
		("Pending", "Pending"),
		("Complete", "Complete"),)

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length = 500)
	price = models.DecimalField(max_digits = 6, decimal_places = 2)
	status = models.CharField(max_length = 8, choices = status_choices, default = "Pending")

	def __str__(self):
		return f"{self.user}: {self.title} for {self.price}"


class Extra(models.Model):

	name = models.CharField(max_length = 50)

	def __str__(self):
		return self.name

