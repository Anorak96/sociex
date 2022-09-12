// LOGIN
const togglePassword = document.getElementById('togglePassword');
const password = document.getElementById('password');
if (togglePassword) {
    togglePassword.addEventListener('click', () => {
        console.log('btn clicked')

        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        
        if (password.type === "password") {
            document.getElementById('togglePassword').className = "fas fa-eye-slash pwshow";
        } else {
            document.getElementById('togglePassword').className = "fas fa-eye pwshow";
        }
    });
}
// POST LIKE================================================================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$('.postLike').click(function (e) {
    e.preventDefault();

    let post_pk = $(this).val()
    const data = { body: chatMess };
    console.log('post :', post_pk)

    $.ajax({
        type: 'POST',
        url: '{% url "post:like_post" %}',
        data: {
            post_id: $(this).val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function (responce) {
            console.log('success', responce)
            let like_num = document.getElementsByClassName("like_count")
            like_num.innerHTML = responce.likes_no
            console.log('like no :', document.getElementsByClassName("like_count").innerHTML, ',', responce.likes_no)
        },
        error: function (xhr, errmsg, err) {

        }
    });
})
// ===========================================================================================================
$(document).ready(function () {
    $('.owl-carousel').owlCarousel({
        loop: true,
        margin: 15,
        dot: true,
        nav: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    })
});
// ===========================================================================================================
const backToTopButton = document.querySelector("#back-to-top-btn");

window.addEventListener("scroll", scrollFunction);

function scrollFunction() {
    if (window.pageYOffset > 100) { // Show backToTopButton
        if (!backToTopButton.classList.contains("btnEntrance")) {
            backToTopButton.classList.remove("btnExit");
            backToTopButton.classList.add("btnEntrance");
            backToTopButton.style.display = "block";
        }
    }
    else { // Hide backToTopButton
        if (backToTopButton.classList.contains("btnEntrance")) {
            backToTopButton.classList.remove("btnEntrance");
            backToTopButton.classList.add("btnExit");
            setTimeout(function () {
                backToTopButton.style.display = "none";
            }, 250);
        }
    }
}

backToTopButton.addEventListener("click", smoothScrollBackToTop);

function smoothScrollBackToTop() {
    const targetPosition = 0;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    const duration = 200;
    let start = null;

    window.requestAnimationFrame(step);

    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        window.scrollTo(0, easeInOutCubic(progress, startPosition, distance, duration));
        if (progress < duration) window.requestAnimationFrame(step);
    }
}

function easeInOutCubic(t, b, c, d) {
    t /= d / 2;
    if (t < 1) return c / 2 * t * t * t + b;
    t -= 2;
    return c / 2 * (t * t * t + 2) + b;
};

// ===========================================================================================================
const spinnerBox = document.getElementById('spinner-box')
const post2 = document.getElementById('post2')
const post_image = document.getElementById('json_image')
const post_caption = document.getElementById('json_caption')
const post_user = document.getElementById('json_user')


$.ajax({
    type: 'GET',
    url: '/post_json',
    success: function(response){
        setTimeout(()=>{
            const data = JSON.parse(response.data)
            console.log('data:', data)
            data.forEach(el=>{
                post2.innerHTML += el.fields.user + ' -- ' + el.fields.caption + '<br>'
                post_image.innerHTML += el.fields.user.profile_pic
                post_caption.innerHTML += el.fields.caption
                post_user.innerHTML += el.fields.user


            })
            spinnerBox.classList.add('not-visible')
            spinnerBox.classList.remove('d-flex')
        }, 500)
    },
    error: function(error){
        setTimeout(()=>{
            console.log(error)
            spinnerBox.classList.add('not-visible')
        }, 500)
    }
})
// ===========================================================================================================
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    handler: function (direction) {
    },

    offset: 'bottom-in-view',

    onBeforePageLoad: function () {
        $('.lds-ripple').show();
    },
    onAfterPageLoad: function () {
        $('.lds-ripple').hide();
    }
});
// ===========================================================================================================
