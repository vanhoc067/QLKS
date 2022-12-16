;(function () {

	'use strict';



	// iPad and iPod detection
	var isiPad = function(){
		return (navigator.platform.indexOf("iPad") != -1);
	};

	var isiPhone = function(){
	    return (
			(navigator.platform.indexOf("iPhone") != -1) ||
			(navigator.platform.indexOf("iPod") != -1)
	    );
	};

	// Main Menu Superfish
	var mainMenu = function() {

		$('#fh5co-primary-menu').superfish({
			delay: 0,
			animation: {
				opacity: 'show'
			},
			speed: 'fast',
			cssArrows: true,
			disableHI: true
		});

	};


	// Offcanvas and cloning of the main menu
	var offcanvas = function() {

		var $clone = $('#fh5co-menu-wrap').clone();
		$clone.attr({
			'id' : 'offcanvas-menu'
		});
		$clone.find('> ul').attr({
			'class' : '',
			'id' : ''
		});

		$('#fh5co-page').prepend($clone);

		// click the burger
		$('.js-fh5co-nav-toggle').on('click', function(){

			if ( $('body').hasClass('fh5co-offcanvas') ) {
				$('body').removeClass('fh5co-offcanvas');
			} else {
				$('body').addClass('fh5co-offcanvas');
			}
			// $('body').toggleClass('fh5co-offcanvas');

		});

		$('#offcanvas-menu').css('height', $(window).height());

		$(window).resize(function(){
			var w = $(window);


			$('#offcanvas-menu').css('height', w.height());

			if ( w.width() > 769 ) {
				if ( $('body').hasClass('fh5co-offcanvas') ) {
					$('body').removeClass('fh5co-offcanvas');
				}
			}

		});

	}



	// Click outside of the Mobile Menu
	var mobileMenuOutsideClick = function() {
		$(document).click(function (e) {
	    var container = $("#offcanvas-menu, .js-fh5co-nav-toggle");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('fh5co-offcanvas') ) {
				$('body').removeClass('fh5co-offcanvas');
			}
	    }
		});
	};


	// Animations

//	var contentWayPoint = function() {
//		var i = 0;
//		$('.animate-box').waypoint( function( direction ) {
//
//			if( direction === 'down' && !$(this.element).hasClass('animated') ) {
//
//				i++;
//
//				$(this.element).addClass('item-animate');
//				setTimeout(function(){
//
//					$('body .animate-box.item-animate').each(function(k){
//						var el = $(this);
//						setTimeout( function () {
//							el.addClass('fadeInUp animated');
//							el.removeClass('item-animate');
//						},  k * 200, 'easeInOutExpo' );
//					});
//
//				}, 100);
//
//			}
//
//		} , { offset: '85%' } );
//	};


	// Document on load.
	$(function(){
		mainMenu();
		offcanvas();
		mobileMenuOutsideClick();


	});


}());



function create_book_room(customer_id, room_id) {
    var checkInDate = document.getElementById("checkInDate").value;
    var checkOutDate = document.getElementById("checkOutDate").value;
    console.log("checkInDate", checkInDate)
    console.log("checkOutDate", checkOutDate)
    console.log("customer_id", customer_id)
    console.log("room_id", room_id)
    fetch("/api/room", {
        method: "post",
        body: JSON.stringify({
            "customers": customer_id,
            "rooms": room_id,
            "checkInDate": checkInDate,
            "checkOutDate": checkOutDate
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        if (data.code == 200) {
                alert("Đặt phòng thành công")
                console.log('success')
            }
            else if (data.code == 400){
                alert("Ngày đặt phòng không được quá 28 ngày sao với ngày nhận")
                console.log('fail')
            }
    })
}


function create_rent(customer_id, room_id, checkInDate, checkOutDate, book_id) {
    console.log("checkInDate", checkInDate)
    console.log("checkOutDate", checkOutDate)
    console.log("customer_id", customer_id)
    console.log("room_id", room_id)
    console.log("book_id", book_id)

    fetch("/api/create_rent", {
        method: "post",
        body: JSON.stringify({
            "customer_id": customer_id,
            "room_id": room_id,
            "checkInDate": checkInDate,
            "checkOutDate": checkOutDate,
            "book_id": book_id
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        if (data.code == 200) {
                alert("Lập phiếu thuê thành công")
                console.log('success')
            }
            else if (data.code == 400){
                alert("Số lượng không được quá 3 người")
                console.log('fail')
            }
    })
}


 function addToCart(id, name, price) {
    fetch("/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }) // js promise
}

function updateCart(productId, obj) {
    fetch(`/api/cart/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res) => res.json()).then((data) => {
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let a = document.getElementsByClassName('cart-amount')
        for (let i = 0; i < a.length; i++)
            a[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.error(err)) // js promise
}

function deleteCart(productId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
         fetch(`/api/cart/${productId}`, {
            method: "delete"
        }).then((res) => res.json()).then((data) => {
            console.info(data)
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let a = document.getElementsByClassName('cart-amount')
            for (let i = 0; i < a.length; i++)
                a[i].innerText = data.total_amount.toLocaleString("en-US")

            let e = document.getElementById(`cart${productId}`)
            e.style.display = "none"
        }).catch(err => console.error(err)) // js promise
    }

}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?") == true) {
        fetch("/api/pay").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload()
        })
    }

}

function pay_the_bill(bill_id) {
    fetch('/api/pay-bill', {
        method: 'post',
        body: JSON.stringify ({
            'id': bill_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data){
        console.info(data)
    })
}

function get_pay_url_momo(bill_id, amount, current_url) {
    console.log("bill_id", bill_id)
    console.log("amount", amount)
    console.log("current_url", current_url)
    fetch('/api/pay_with_momo', {
        method: 'post',
        body: JSON.stringify({
            'id': bill_id,
            'amount': amount,
            'current_url': current_url
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res){
        console.log(res);
        return res.json();
    }).then(function(data) {
        console.log(data.code);
        console.info(data)
        if (data.code == 200) {
            console.log('success');
            window.location.replace(data.pay_url);
        }
        else if (data.code == 400) {
            console.log('fail');
            document.getElementById("btnPayMomo").disabled = "true"
        }
    }).catch(function(err) {
        console.error(err);
    });
}

function pay_the_bill(bill_id) {
    fetch('/api/pay-bill', {
        method: 'post',
        body: JSON.stringify ({
            'id': bill_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        console.log(data.code)
        popup = document.querySelector('.popup_detail-pay-the-bill');
        title_popup = document.querySelector('.title_popup_detail-pay-the-bill')
        popup.classList.add("show_popup_detail");
        if (data.code == 200){
            console.log('success');
            dis = document.getElementsByClassName("btnPay")
            for (d of dis) {
                d.style.display = "none";
            }
            title_popup.innerHTML = "Thanh toán thành công!";
            popup.style.border = '5px solid green';
            popup.classList.add("show_popup_detail");

        }
        else if (data.code == 400)
            console.log('fail');
    }).catch(err => console.error(err))

}

function like(customer_id, room_id, like_id) {
    fetch("/api/create_like", {
    method: "post",
    body: JSON.stringify({
        "customers": customer_id,
        "rooms": room_id,
    }),
    headers: {
        "Content-Type": "application/json"
    }
    }).then((res) => res.json()).then((data) => {
        console.info(data)
    })
    /*var color = document.getElementById("createLike1")
    console.log("color: ", color)
    color.style.color = "blue"*/
    window.location.reload()
}

function update_like(like_id, active) {
    fetch(`/api/like/${like_id}`, {
    method: "put",
    body: JSON.stringify({
        "active": active
    }),
    headers: {
        "Content-Type": "application/json"
    }
    }).then((res) => res.json()).then((data) => {
        console.info(data)
    })
    /*if(active == 1){
        var color1 = document.getElementById("createLike2")
        color1.style.color = "#ffffff"
        var color2 = document.getElementById("createLike3")
        color2.style.color = "#ffffff"
    }else{
        var color1 = document.getElementById("createLike2")
        color1.style.color = "blue"
        var color2 = document.getElementById("createLike3")
        color2.style.color = "blue"
    }*/
    window.location.reload()
}

function addComment(){
    let content_comment = document.getElementById('content-of-comment')
    let cus_comment = document.getElementById('name-of-patient-comment')
    let star_comment = document.querySelector('input[name="rating"]:checked').value;

    if(content_comment !== null){
        fetch('/api/comment',{
            method: 'post',
            body:JSON.stringify({
                'content_comment':content_comment.value,
                'cus_comment':cus_comment.value,
                'star_comment':star_comment
            }),
            headers:{
                'Content-Type':'application/json'
            }
        }).then(res => res.json()).then(data=>{
            if (data.status == 201){
                let c = data.comment
                let area = document.getElementById('commentArea')
                console.log(c.cus_comment)
                console.log(c.content_comment)
                area.innerHTML =`
                    <div class="swiper-slide" id="commentArea">
                      <div class="name-patient-comment">${c.cus_comment}</div>
                      <div class="content-comment">${c.content_comment}</div>
                      <div class="rate-comment">
                        for (let i = 0; i < Number(star_comment); i++){
                            <i class="fas fa-star" style="color:blue"></i>
                        }
                        for (let i = 0; i < 5- Number(star_comment); i++){
                            <i class="far fa-star" style="color:blue"></i>
                        }
                      </div>
                    </div>
                `+area.innerHTML
                location.reload();
            }else if (data.status == 404){
                alert(data.error_ms)
            }
    })
    .catch(function(err){
        console.error(err)
    })
    }
}


