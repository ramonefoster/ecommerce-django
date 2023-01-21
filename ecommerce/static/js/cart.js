var update_buttons = document.getElementsByClassName('update-cart')

for (i=0; i < update_buttons.length; i++){
    update_buttons[i].addEventListener('click', function(){
        var product_id = this.dataset.product
        var action = this.dataset.action

        console.log(user)
        if (user === 'AnonymousUser'){
            addCookieItem(product_id, action)
        } else {
            updateUserOrder(product_id, action)
        }
    })
}

function addCookieItem(product_id, action){
    if (action=='add'){
        if (cart[product_id] == undefined){
            cart[product_id] = {'quantity':1}
        }else {
            cart[product_id]['quantity']+=1
        }
    }
    if (action=='remove'){
        cart[product_id]['quantity']-=1
        if (cart[product_id]['quantity'] <= 0){
            delete cart[product_id]
        }
    }
    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}

function updateUserOrder(product_id, action){
    console.log('User logged in', user)

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'product_id': product_id,
                'action': action})
    }).then((response) => {
        return response.json()
    }).then((data)=>{
        location.reload()
    })
}