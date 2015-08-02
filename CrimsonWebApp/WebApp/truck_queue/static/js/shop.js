var orderItems = {};

$(document).ready(function() {
	$("button").click(function() {
		var foodItemID = this.id;
		if (foodItemID != "order-submit") {
			var foodItemName = this.name;
			var foodItemPrice = this.value;
			var myOrder = document.getElementById("myOrder");
			if (orderItems[foodItemName] == undefined) {
				foodPriceItem = $("#price-" + foodItemID);
				
				item = { 
					"quantity" : 1,
					"price" : foodItemPrice
				}

				orderItems[foodItemName] = item;


				var foodItem = myOrder.insertRow(-1);

				foodItem.id = "food-item-" + foodItemID;

				var name = foodItem.insertCell(0);
				name.innerHTML = foodItemName;

				var price = foodItem.insertCell(1);
				price.innerHTML = foodItemPrice;

				var quantity = foodItem.insertCell(2);
				quantity.id = "quantity-" + foodItemID;
				quantity.innerHTML = orderItems[foodItemName].quantity;

				var remove = foodItem.insertCell(3);
				var removeButton = document.createElement("href");

				removeButton.id = "delete-button-" + foodItemID;
				removeButton.value = foodItemID;
				removeButton.onclick = function() {
					var rowNumber = this.value;
					var row = document.getElementById("food-item-" + rowNumber);
					$(row).remove();
					delete orderItems[foodItemName]
					calculateTotalPrice(orderItems);
					convertTotalPriceToHTML(orderItems);
				}
				removeButton.innerHTML = '<span class="glyphicon glyphicon-remove"></span>';
				$(remove).append(removeButton);
				convertTotalPriceToHTML(orderItems);
			}
			else {
				item = orderItems[foodItemName];
				item.quantity = item.quantity + 1;					
				var quantityColumn = document.getElementById("quantity-" + foodItemID);
				quantityColumn.innerHTML = item.quantity;
				$("#number-of-item-" + foodItemID).innerHTML = orderItems[foodItemName];
				convertTotalPriceToHTML(orderItems);					
			}
			console.log(calculateTotalPrice(orderItems));
			document.getElementById("total-price").innerHTML;
		}
	});
});

function calculateTotalPrice(order) {
	var totalPrice = 0.00;
	var innerObject;
	for (var item in order) {
		innerObject = order[item];
		console.log(innerObject.quantity);
		console.log(innerObject.price);
		totalPrice += innerObject.quantity * innerObject.price;
	}
	return totalPrice.toFixed(2);
}

function convertTotalPriceToHTML(order) {
	var totalPrice = calculateTotalPrice(order);
	document.getElementById("total-price").innerHTML = totalPrice;
}

window.onkeypress = function(event) {
    if(event.keyCode == 49) {
        $.ajax({url: "demo"}).done(function() {});
    }
}