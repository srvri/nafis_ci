//custom.js
(function ($) {
    "use strict";

    $(document).ready(function () {
        // 1. Preloader
        $(window).on('load', function () {
            console.log("Preloader starting...");
            $('.preloader').delay(500).slideUp('slow', function () {
                console.log("Preloader finished.");
            });
        });

        // 2. Navbar (Headroom)
        if ($.fn.headroom) {
            console.log("Headroom plugin loaded, initializing navbar...");
            $(".navbar").headroom();
        } else {
            console.warn("Headroom plugin is not loaded!");
        }

        // 3. Navbar Collapse
        console.log("Setting up navbar collapse...");
        $('.navbar-collapse a').on('click', function () {
            $(".navbar-collapse").collapse('hide');
            console.log("Navbar collapsed after click.");
        });

        // 4. Slideshow (Slick)
        const $slideshow = $('.nafis-slideshow');
        const $slideItems = $slideshow.find('.nafis-slide-item');
        console.log("تعداد اسلایدها:", $slideItems.length);

        // تست DOM برای اطمینان از لود شدن اسلایدها
        $slideItems.each(function (index) {
            const imgSrc = $(this).find('img').attr('src');
            console.log("اسلاید " + (index + 1) + ": " + imgSrc);
        });

        // اجرا فقط اگر اسلایدی وجود داشته باشه
        if ($slideItems.length > 0) {
            if ($.fn.slick) {
                console.log("Slick plugin loaded, initializing slideshow...");
                $slideshow.slick({
                    rtl: true,
                    autoplay: true,
                    autoplaySpeed: 3000,
                    infinite: true,
                    arrows: true,
                    fade: false,
                    dots: true,
                    slidesToShow: 1,
                    slidesToScroll: 1
                });
            } else {
                console.error("Slick plugin is not loaded!");
            }
        } else {
            console.warn("No slides available to initialize slideshow!");
        }

        // 5. Product Carousel - Bootstrap Multi-Item Carousel
        console.log("Initializing Bootstrap product carousels...");
        
        $('.carousel-showmanymoveone').each(function() {
            var $carousel = $(this);
            var carouselId = $carousel.attr('id');
            
            console.log("Setting up carousel:", carouselId);
            
            // شروع carousel با تنظیمات
            $carousel.carousel({
                interval: 3000,
                pause: 'hover'
            });
            
            // کلون کردن آیتم‌ها برای نمایش چندتایی
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

        // 6. Testimonial Carousel - موقتاً غیرفعال
        /*
        const $testimonial = $('.slick-testimonial');
        if ($testimonial.length && $.fn.slick) {
            console.log("Initializing testimonial carousel...");
            $testimonial.slick({
                arrows: false,
                dots: true,
                rtl: true
            });
        } else {
            console.warn("Testimonial carousel not initialized (Slick or element missing)!");
        }
        */
    });
})(window.jQuery);