// Execute when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {

	// Show prices for the pizza, sub and platter that is selected by default
	priceCalculator(document.querySelector("#pizza_price"), pizzaData());
	priceCalculator(document.querySelector("#sub_price"), subData());
	priceCalculator(document.querySelector("#platter_price"), platterData());

	
	// JS for the "pizzas" form

	// grab all HTML elements that are needed
	var pizza_form = document.querySelector("#pizza_form");
	var pizza_toppings = document.querySelector("#pizza_toppings");
	var topping_list = document.querySelector("#topping_list");
	var topping_name = document.querySelector("#topping_name");
	var topping_error = document.querySelector("#topping_error");
	var pizza_button = document.querySelector("#pizza_button");

	// Recalculate prices every time the form changes
	pizza_form.onchange = () => {

		priceCalculator(document.querySelector("#pizza_price"), pizzaData());
	}

	// Sort out toppings
	pizza_toppings.onchange = () => {

		// If the user wants no additional toppings, hide them
		if (pizza_toppings.value == 0) {

			topping_list.style.visibility = "hidden";
			topping_name.disabled = true;
			topping_name.selectedIndex = -1;
		}

		// Otherwise show the list of toppings
		else {

			topping_list.style.visibility = "visible";
			topping_name.disabled = false;
		}

		// Check if the selected number of toppings matches the number the user has decided on earlier
		// If not, warn the user
		toppingChecker();

	}
	// Do the earlier check every time the the user selects/unselects a topping
	topping_name.onchange = () => {
		
		toppingChecker();
	};

	// JS for the "subs" form
	
	// Grab the form elements that are needed
	var sub_name = document.querySelector("#sub_name");
	var sub_extras = document.querySelector("#sub_extras");
	var sub_form = document.querySelector("#sub_form");
	var extra_name = document.querySelector("#extra_name");
	var sub_size = document.querySelector("#sub_size");
	var extra_cheese = document.querySelector("#extra_cheese");

	// Change the value of the "extra cheese" element appropriately whenever it is checked/unchecked
	extra_cheese.onchange = () => {

		if (extra_cheese.checked) {

			extra_cheese.value = "yes";
		}
		else {

			extra_cheese.value = "no";
		
		}
	}

	// Execute every time the users change the sub they want
	sub_name.onchange = () => {

		// If the user has selected the right sub, show them the extra-selector
		if (sub_name.value == "Steak + Cheese") {

			sub_extras.style.visibility = "visible";
		}
		// If the user has selected some other sub, keep the extra-selector hidden
		else {

			sub_extras.style.visibility = "hidden";
			
			extra_name.selectedIndex = -1;
		}
		// This particular sub is only available in large size
		if (sub_name.value == "Sausage, Peppers & Onions") {

			// Lock the size selector in at the "large" value
			sub_size.selectedIndex = 1;
			sub_size.disabled = true;

		}
		// Let users select the size for any other sub
		else {

			sub_size.disabled = false;
		}

	}

	// Recalculate price every time the form changes
	sub_form.onchange = () => {	

		priceCalculator(document.querySelector("#sub_price"), subData());
		
	};

	// JS for the "dinner platters" form

	// Grab the form itself
	var platter_form = document.querySelector("#platter_form");

	// Recalculate price every time the form changes
	platter_form.onchange = () => {

		priceCalculator(document.querySelector("#platter_price"), platterData());
	}

	// JS for the shopping cart

	// Disable buttons if the cart is empty
	if(document.querySelectorAll(".delete-button").length == 0) {

			document.querySelector("#empty_cart").disabled = true;
			document.querySelector("#place_order").disabled = true;
		};

		// Execute when a "delete" button is clicked
		document.querySelectorAll(".delete-button").forEach(button => {
			button.onclick = () => {
				
				// Delete the title that is associated with the delete button and reload the page
				var my_id = button.dataset.my_id;
				
				postCart(deleteCart(my_id));
				location.reload();
			}

		});


		// Empty shopping cart when the button is clicked, then reload the page
		document.querySelector("#empty_cart").onclick = () => {

			postCart(emptyCart());
			location.reload();

		};

		// Place order when the button is clicked, then reload the page
		document.querySelector("#place_order").onclick = () => {

			postCart(placeOrder());
			location.reload();
		}

// Check toppings
function toppingChecker() {
	
	// The number of selected toppings should equal the number the user has selected earlier
	const toppingLimit = pizza_toppings.value;
	
	// Dismiss the check if the user has decided to add no toppings
	if (toppingLimit == 0) {

		var selectedToppings = 0;
	}
	// Otherwise, warn the user if there is a mismatch and disable the submit button
	else {
		var selectedToppings = topping_name.selectedOptions.length;
	}

	if (toppingLimit != selectedToppings) {
		
		topping_error.style.visibility = "visible";
		pizza_toppings.style.border = "1px solid red";
		topping_name.style.border = "1px solid red";
		
		pizza_button.disabled = true;

	}
	// Hide warnings once the user has addressed the issue and enable the submit button
	else {
		
		topping_error.style.visibility = "hidden";
		pizza_toppings.style.border = "1px solid #ced4da";
		topping_name.style.border = "1px solid #ced4da";
		
		pizza_button.disabled = false;
	}
};

// Calculates prices
function priceCalculator(div, my_function) {


	// Send a POST request to the server
	const request = new XMLHttpRequest();
	request.open("POST", "/price/");
	
	
	request.onload = () => {
		
		// The server's response is the calculated price itself
		div.innerHTML = request.response;
	}
	
	// The data sent to the server varies based on which food's (pizza, sub or platter) price is in question
	const data = my_function;

	// Add a csrf-token to the request headers so that Django accepts the request
	var csrftoken = Cookies.get("csrftoken");
	request.setRequestHeader("X-CSRFToken", csrftoken);

	// Send the data
	request.send(data);

}

// Organizes information collected from the pizza form
function pizzaData() {

	const data = new FormData();
	
	// Let the server know which kind of food it needs to calculate a price for
	data.append('food_type', 'pizzas');

	// Add relevant info to the formdata
	data.append('pizza_size', document.querySelector("#pizza_size").value);
	data.append('pizza_type', document.querySelector("#pizza_type").value);
	data.append('pizza_toppings', document.querySelector("#pizza_toppings").value);

	return data;
}

// Organizes information collected from the sub form
function subData() {

	const data = new FormData();
	
	// Let the server know which kind of food it needs to calculate a price for
	data.append('food_type', 'subs');

	// Add relevant info to the formdata
	data.append('sub_size', document.querySelector("#sub_size").value);
	data.append('sub_name', document.querySelector("#sub_name").value);
	data.append('sub_extras', document.querySelector("#extra_name").selectedOptions.length);	
	data.append('extra_cheese', document.querySelector("#extra_cheese").value);

	return data;
}

// Organizes information collected from the platter form
function platterData() {

	const data = new FormData();
	// Let the server know which kind of food it needs to calculate a price for
	data.append('food_type', 'platters');

	// Add relevant info to the formdata
	data.append('platter_size', document.querySelector("#platter_size").value);
	data.append('platter_name', document.querySelector("#platter_name").value);

	return data;
}

// Sends POST requests related to the shopping cart
function postCart(my_function) {

	// Send a POST request
	const request = new XMLHttpRequest();
		request.open("POST", "/cart/");

		// The data sent to the server varies on what action does the user want to take (delete an element,
		// empty the cart, place an order)
		const data = my_function;

		// Add csrf-token to the request's header
		var csrftoken = Cookies.get("csrftoken");
		request.setRequestHeader("X-CSRFToken", csrftoken);

		// Send the data
		request.send(data);
}

// Organizes the data needed to delete an element from the shopping cart
function deleteCart(my_id) {

	const data = new FormData();
	
	// Let the server know which action is the user taking
	data.append("post_type", "delete");
	
	// Add the selected element's id to the formdata
	data.append("my_id", my_id);
	
	return data;
}

// Organizes the data needed to empty the shopping cart
function emptyCart() {

	const data = new FormData();
	
	// Let the server know what's happening
	data.append("post_type", "empty");
	
	return data;
}
// Organizes the data needed to place an order
function placeOrder() {

	const data = new FormData();
	
	// Let the server know what is happening
	data.append("post_type", "place_order");

	return data;
}