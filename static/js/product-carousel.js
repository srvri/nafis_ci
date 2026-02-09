// product-carousel.js
// اسلایدر محصولات با Bootstrap Carousel

(function($) {
    "use strict";
    
    $(document).ready(function() {
        console.log("Product carousel script loaded");
        
        // پیدا کردن تمام اسلایدرهای محصولات
        $('.carousel-showmanymoveone').each(function() {
            var $carousel = $(this);
            var carouselId = $carousel.attr('id');
            
            console.log("Initializing carousel:", carouselId);
            
            // شروع carousel با تنظیمات
            $carousel.carousel({
                interval: 3000,
                pause: 'hover'
            });
            
            // کلون کردن آیتم‌ها برای اسلایدر چند تایی
            $carousel.find('.item').each(function() {
                var itemToClone = $(this);
                
                // کلون 5 آیتم بعدی
                for (var i = 1; i < 6; i++) {
                    itemToClone = itemToClone.next();
                    
                    // اگر به آخر رسیدیم، از اول شروع کن
                    if (!itemToClone.length) {
                        itemToClone = $(this).siblings(':first');
                    }
                    
                    // کلون فرزند اول و اضافه کردن کلاس
                    itemToClone.children(':first-child').clone()
                        .addClass("cloneditem-" + i)
                        .appendTo($(this));
                }
            });
            
            console.log("Carousel initialized:", carouselId);
        });
    });
})(jQuery);