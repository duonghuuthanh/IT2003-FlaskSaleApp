function addToCart(id, name, price) {
    fetch("/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) { return res.json() }).then(function(data) {
        let q = data.total_quantity
        let d = document.getElementsByClassName('cart-quantity')[0]
        d.innerText = q
    })
}

function updateCart(productId, obj) {
    fetch(`/cart/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let q = data.total_quantity
        let d = document.getElementsByClassName('cart-quantity')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = q
        let amount = document.getElementsByClassName('cart-amount')[0]
        amount.innerText = data.total_amount
    })
}