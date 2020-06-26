function confirmOrder() {
  // sent a request to django app to confirm order
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "confirm-order-final");
    request.send();
  });
}

function cancelOrder() {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "cancel-order");
    request.send();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // adding behaviour for order buttons
  const btn_confirm_order = document.querySelector("#btn-confirm-order");
  if (btn_confirm_order != null) {
    // if confirm order button is in order page: define behaviour
    btn_confirm_order.onclick = (e) => {
      // run confirm order function and go back to main page if successful
      confirmOrder()
        .then(function(result) {
          window.location.replace("/");
        });
    };
  }

  const btn_cancel_order = document.querySelector("#btn-cancel-order");
  if (btn_cancel_order != null) {
    btn_cancel_order.onclick = (e) => {
      cancelOrder()
        .then(function(result) {
          window.location.replace("/");
        });
    };
  }
});
