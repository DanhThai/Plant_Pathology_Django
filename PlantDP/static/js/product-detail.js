$(document).ready(function () {
    $(".add-cart-btn-multi").click(function () {
        var product_id = $(this).data("product");
        var action = $(this).data("action");
        var quantity = Number($(".quantity__number").val());
        addProductCart(product_id, action, quantity);
    });

    $(".add-cart-btn").each(function () {
        $(this).click(function () {
            var product_id = $(this).data("product");
            var action = $(this).data("action");
            addProductCart(product_id, action, 1);
        });
    });
});

function EditQuantity(value) {
    var quantity = Number($(`.quantity__number`).val());
    if (value == "-") {
        if (quantity > 1) $(`.quantity__number`).val(quantity - 1);
    } else {
        $(`.quantity__number`).val(quantity + 1);
    }
}

function changeImage(id) {
    console.log(id);
    var loc = $(`#${id}`).attr("src");
    $('#image-focus').attr("src",loc);
}



function addProductCart(product_id, action, quantity) {
    base_url = "http://127.0.0.1:8000/user/shopping-cart/update";
    fetch(base_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify({
            product_id: product_id,
            quantity: quantity,
            action: action,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        $('#alert-message').prepend(
            `<div class="alert-messages">\
            <i class="fa-solid fa-circle-check" style="width: 25px; height: 25px;"></i>\
            <div class="message-body">\
                <p class="message__title">Thành công</p>\
                <p class="message_content">${data.message}</p>\
            </div>\
            <i class="fa-solid fa-xmark close-message" onclick="closeMessage()"></i>\
            </div>`)
        $('#cart-number').text(data.cart_number)
    });
}
