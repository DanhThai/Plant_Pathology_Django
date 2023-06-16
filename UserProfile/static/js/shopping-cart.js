
function removeVnd(str){
  var num = str.split(" ");
  return Number(num[0]);
}

function EditQuantity(value, cart_item_id, cart_id){
  var cart_item = `cart-item-${cart_item_id}`
  var quantity = Number($(`.quantity__number.${cart_item}`).val());
  var price = Number(removeVnd($(`.product-price.${cart_item}`).text()));
  var cart_price = Number(removeVnd($(`.cart-${cart_id}-price`).text()));

  if(value == '-'){
    if(quantity>1)
      $(`.quantity__number.${cart_item}`).val(quantity - 1);
      $(`.cart-${cart_id}-price`).text(cart_price - price);
      total_price = total_price-price;
      $(`.price-total.cart-${cart_id}`).text(total_price);
  }
  else{
    $(`.quantity__number.${cart_item}`).val(quantity + 1);
    $(`.cart-${cart_id}-price`).text(cart_price + price);
    total_price = total_price+price;
    $(`.price-total.cart-${cart_id}`).text(total_price);
  }
}

if($('#paypal-button-container').length == 0){
  console.log("Paypal");
  base_url = 'http://127.0.0.1:8000/user/shopping-cart/'
  paypal.Buttons({
    style: {
      layout:  'vertical',
      color:   'gold',
      shape:   'rect',
      label:   'pay'
    },
      // Order is created on the server and the order id is returned
      createOrder() {
        return fetch(base_url + `checkout/${cart_id}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
          },
          body: JSON.stringify({
            totalPrice: total_price
          }),
        })
        .then(
          (response) => response.json())
        .then(
          (order) => order.id)
        ;
      },
      // Finalize the transaction on the server after payer approval
      onApprove(data) {
        return fetch(base_url + `capture/?orderId=${data.orderID}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          }
        })
        .then((response) => response.json())
        .then((orderData) => {
          // Successful capture! For dev/demo purposes:
          console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
          const transaction = orderData.purchase_units[0].payments.captures[0];
          alert(`Transaction ${transaction.status}: ${transaction.id}\n\nSee console for all available details`);
          // When ready to go live, remove the alert and show a success message within this page. For example:
          window.location.href = base_url + '?isPaid=True';
        });
      }
    }).render('#paypal-button-container');
}