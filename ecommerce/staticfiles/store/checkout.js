function startPayment(razorpayKey, orderId, amount) {

  var options = {
    "key": razorpayKey,
    "amount": amount,
    "currency": "INR",
    "name": "My Store",
    "description": "Order Payment",
    "order_id": orderId,

    "handler": function (response) {
      // Payment successful
      document.getElementById("razorpay_payment_id").value = response.razorpay_payment_id;
      document.getElementById("razorpay_order_id").value = response.razorpay_order_id;
      document.getElementById("razorpay_signature").value = response.razorpay_signature;

      document.getElementById("payment-form").submit();
    },

    "theme": {
      "color": "#0d6efd"
    }
  };

  var rzp = new Razorpay(options);
  rzp.open();
}
function payNow(razorpayKey, orderId, amount) {
  startPayment(razorpayKey, orderId, amount);
}
document.getElementById("pay-now-btn").addEventListener("click", function(e){
  e.preventDefault();
  var razorpayKey = this.getAttribute("data-razorpay-key");
    var orderId = this.getAttribute("data-order-id");
    var amount = this.getAttribute("data-amount");
    payNow(razorpayKey, orderId, amount);
});