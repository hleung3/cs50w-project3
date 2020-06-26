function checkData(form_name,data) {
    var missing = false;
    // check if fields are empty
    for (var pair of data.entries()) {
      if (pair[0] == "csrfmiddlewaretoken") {
      }
      else if (pair[1] == "" || !pair[1]) {
        alert(`missing data please fill out ${form_name} form`);
        missing = true;
        return !(missing);
      }
    }
    if (form_name == "Pizza") {
      // check if toppings selected match number selected
      const list_toppings = data.getAll("list_toppings");
      // let test = list_toppings.every(function(e) {
      //   return typeof e;
      // });
      console.log(list_toppings,list_toppings[0]);
      const num_toppings = parseInt(data.get("num_toppings"));
      if ((num_toppings == parseInt(list_toppings[0])) &&
          (num_toppings == 0)) {
        // Cheese pizza exception (num_topp == 0) and (list_top selected default option 0)
      } else if (list_toppings.includes("0")) {
        alert("remove select.. from toppings");
        return false;
      } else if (num_toppings != list_toppings.length) {
        alert("please select the correct number of toppings");
        return false;
      }
    }
    return !(missing);
}

function addToCart(data) {
  // make request to django app (orders/add_to_cart)
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "add-to-cart");
    request.send(data);
  });
}



function setOrderPrice(order_price) {
  // update user's current order price
  const span = document.querySelector("#order-price");
  span.innerText = "$" + order_price;

  const a = span.closest("a");
}

document.addEventListener("DOMContentLoaded", () => {

  const subtype = document.querySelector("#sub-type");
  subtype.addEventListener("click", (e) => {
    document.querySelectorAll(".steak-cheese").forEach((element) => {
      if ((element.style.display == "none") &&
      (subtype.options[subtype.selectedIndex].text == "Steak + Cheese")) {
        element.style.display = "block";
      } else {
        element.style.display = "none";
      }
    });
  });
  //
  // define "Add to Order" button behaviour
  document.querySelectorAll(".order-button").forEach((element) => {
    element.onclick = (e) => {
      const form_name = e.target.dataset.formName;
      if (form_name == "Pizza") {
        const pizza_form = document.querySelector("#pizza-form");
        let data = new FormData(pizza_form);
        data.append("product_class",e.target.dataset.productClass);
        const pizza_num = document.querySelector("#pizza-number").value;
        data.append("quantity",pizza_num);
        if (checkData(form_name,data)) {
          addToCart(data)
            .then(function(result) {
              alert("added to cart");
              setOrderPrice(result.order_price);
            })
        }
      }
      else if (form_name == "Sub") {
        let data = new FormData(document.querySelector("#sub-form"));
        data.append("product_class",e.target.dataset.productClass);
        if (checkData(form_name,data)) {
          addToCart(data)
            .then(function(result) {
              alert("added to cart");
              setOrderPrice(result.order_price);
            })
        }
      }
      else if (form_name == "Platter") {
        let data = new FormData(document.querySelector("#platter-form"));
        data.append("product_class",e.target.dataset.productClass);
        if (checkData(form_name,data)) {
          addToCart(data)
            .then(function(result) {
              alert("added to cart");
              setOrderPrice(result.order_price);
            })
        }
      }
      else {
        // salad and pasta share the same format
        let data = new FormData(document.querySelector(`#${form_name}-form`));
        data.append("product_class",e.target.dataset.productClass);
        if (checkData(form_name,data)) {
          addToCart(data)
            .then(function(result) {
              alert("added to cart");
              setOrderPrice(result.order_price);
            })
        }
      }
      return false;
    };
  });
});
