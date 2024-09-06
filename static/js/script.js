$( document ).ready(function() {
    var w = window.innerWidth;

    if(w > 767){
        $('#menu-jk').scrollToFixed();
    }else{
    }



})

$(document).ready(function(){
    $("#testimonial-slider").owlCarousel({
        items:2,
        itemsDesktop:[1000,2],
        itemsDesktopSmall:[979,2],
        itemsTablet:[768,1],
        pagination:false,
        navigation:true,
        navigationText:["",""],
        autoPlay:true
    });
});



$(document).ready(function(){

    $(".filter-button").click(function(){
        var value = $(this).attr('data-filter');

        if(value == "all")
        {
            $('.filter').show('1000');
        }
        else
        {
            $(".filter").not('.'+value).hide('3000');
            $('.filter').filter('.'+value).show('3000');

        }
    });

    if ($(".filter-button").removeClass("active")) {
$(this).removeClass("active");
}
$(this).addClass("active");

});

document.addEventListener('DOMContentLoaded', function () {
    let currentIndex = 0;
    const productsPerPage = 4;
    const productItems = document.querySelectorAll('.product-item');

    function updateProductDisplay() {
        productItems.forEach((item, index) => {
            if (index >= currentIndex && index < currentIndex + productsPerPage) {
                item.classList.remove('d-none');
            } else {
                item.classList.add('d-none');
            }
        });
    }

    function updateButtons() {
        const prevButton = document.getElementById('prev-btn');
        const nextButton = document.getElementById('next-btn');

        if (prevButton) {
            prevButton.disabled = (currentIndex === 0);
        }

        if (nextButton) {
            nextButton.disabled = (currentIndex + productsPerPage >= productItems.length);
        }
    }

    const prevButton = document.getElementById('prev-btn');
    const nextButton = document.getElementById('next-btn');

    if (prevButton) {
        prevButton.addEventListener('click', function() {
            if (currentIndex > 0) {
                currentIndex -= productsPerPage;
                updateProductDisplay();
                updateButtons();
            }
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', function() {
            if (currentIndex + productsPerPage < productItems.length) {
                currentIndex += productsPerPage;
                updateProductDisplay();
                updateButtons();
            }
        });
    }

    // نمایش اولیه محصولات و تنظیم دکمه‌ها
    updateProductDisplay();
    updateButtons();
});
