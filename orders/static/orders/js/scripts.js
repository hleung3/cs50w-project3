
function getOrderPrice() {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "get-current-order-price");

    request.send();
  });
}



function setOrderPrice(order_price) {
  // update user's current order price
  const span = document.querySelector("#order-price");
  span.innerText = "$" + order_price;

  const a = span.closest("a");
}


document.addEventListener("DOMContentLoaded", () => {
  // Get current order price
  getOrderPrice()
    .then(function(result) {
      setOrderPrice(result.order_price);
    });

});
