// Image slider for Home Page
// Last upadted: 3/17/25
// Mike Adams

const swiper = new Swiper('.swiper', {
    direction: 'horizontal',
    loop: true,
    loopPreventsSliding: false,
    effect: "coverflow",
    grabCursor: true,
    centeredSlides: true,
    centeredSlidesBounds: true,
    slidesPerView: "auto",
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    coverflowEffect: {
        rotate: 15,
        stretch: 0,
        depth: 100,
        modifier: 1,
        slideShadows: false,
    },
    pagination: {
        el: '.swiper-pagination',
    },
    autoplay: {
        delay: 7000,
        pauseOnMouseEnter: true,
    },
    speed: 300,
});
