'use strict'

//Preloader
var preloader = $('#spinner-wrapper');
$(window).on('load', function() {
    var preloaderFadeOutTime = 500;

    function hidePreloader() {
        preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
});

jQuery(document).ready(function($) {

    //Incremental Coutner
    if ($.isFunction($.fn.incrementalCounter))
        $("#incremental-counter").incrementalCounter();

    //For Trigering CSS3 Animations on Scrolling
    if ($.isFunction($.fn.appear))
        $(".slideDown, .slideUp").appear();

    $(".slideDown, .slideUp").on('appear', function(event, $all_appeared_elements) {
        $($all_appeared_elements).addClass('appear');
    });

    //For Header Appearing in Homepage on Scrolling
    var lazy = $('#header.lazy-load')

    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 200) {
            lazy.addClass('visible');
        } else {
            lazy.removeClass('visible');
        }
    });

    //Initiate Scroll Styling
    if ($.isFunction($.fn.scrollbar))
        $('.scrollbar-wrapper').scrollbar();

    if ($.isFunction($.fn.masonry)) {

        // fix masonry layout for chrome due to video elements were loaded after masonry layout population
        // we are refreshing masonry layout after all video metadata are fetched.
        var vElem = $('.img-wrapper video');
        var videoCount = vElem.length;
        var vLoaded = 0;

        vElem.each(function(index, elem) {

            //console.log(elem, elem.readyState);

            if (elem.readyState) {
                vLoaded++;

                if (count == vLoaded) {
                    $('.js-masonry').masonry('layout');
                }

                return;
            }

            $(elem).on('loadedmetadata', function() {
                vLoaded++;
                //console.log('vLoaded',vLoaded, this);
                if (videoCount == vLoaded) {
                    $('.js-masonry').masonry('layout');
                }
            })
        });


        // fix masonry layout for chrome due to image elements were loaded after masonry layout population
        // we are refreshing masonry layout after all images are fetched.
        var $mElement = $('.img-wrapper img');
        var count = $mElement.length;
        var loaded = 0;

        $mElement.each(function(index, elem) {

            if (elem.complete) {
                loaded++;

                if (count == loaded) {
                    $('.js-masonry').masonry('layout');
                }

                return;
            }

            $(elem).on('load', function() {
                loaded++;
                if (count == loaded) {
                    $('.js-masonry').masonry('layout');
                }
            })
        });

    } // end of `if masonry` checking


    //Fire Scroll and Resize Event
    $(window).trigger('scroll');
    $(window).trigger('resize');
});

/**
 * function for attaching sticky feature
 **/

function attachSticky() {
    // Sticky Chat Block
    $('#chat-block').stick_in_parent({
        parent: '#page-contents',
        offset_top: 70
    });

    // Sticky Right Sidebar
    $('#sticky-sidebar').stick_in_parent({
        parent: '#page-contents',
        offset_top: 70
    });

}

// Disable Sticky Feature in Mobile
$(window).on("resize", function() {

    if ($.isFunction($.fn.stick_in_parent)) {
        // Check if Screen wWdth is Less Than or Equal to 992px, Disable Sticky Feature
        if ($(this).width() <= 992) {
            $('#chat-block').trigger('sticky_kit:detach');
            $('#sticky-sidebar').trigger('sticky_kit:detach');

            return;
        } else {

            // Enabling Sticky Feature for Width Greater than 992px
            attachSticky();
        }

        // Firing Sticky Recalculate on Screen Resize
        return function(e) {
            return $(document.body).trigger("sticky_kit:recalc");
        };
    }
});

// Fuction for map initialization
function initMap() {
  var uluru = {lat: 12.927923, lng: 77.627108};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: uluru,
    zoomControl: true,
    scaleControl: false,
    scrollwheel: false,
    disableDoubleClickZoom: true
  });
  
  var marker = new google.maps.Marker({
    position: uluru,
    map: map
  });
}
$("document").ready(function () {
    function newsfeed() {
        $.ajax({
            type: "GET",
            url: "/tweet/home/",
            success: function (data) {
                if (data.length == 0) {
                    $('#row-main').empty()
                    $('#row-main').append('<div class="alert alert-info">No Lists to display.</div>')
                    $('#header-section').empty()
                    $('#header-section').append('<h2>ToDo Lists</h2><hr class="bottom-line"><button id="listnew" class="btn btn-success btn-sm"><i class="fa fa-list fa-fw"></i> New List</button>')
                }
                else {
                    $.get('/static/listsf.html', function (htm) {
                        $('#row-main').empty()
                        $('#header-section').empty()
                        $('#header-section').append('<h2>ToDo Lists</h2><hr class="bottom-line"><button id="listnew" class="btn btn-success btn-sm"><i class="fa fa-list fa-fw"></i> New List</button>')
                        $.tmpl(htm, data).appendTo("#row-main")
                    });
                }
            },
        });
    }
    $("body").on('submit', '#loginForm', function (e) {
        e.preventDefault()
        var credentials = {}
        credentials['email'] = $("#loginid").val()
        credentials['password'] = $("#loginpsw").val()
        $.ajax({
            type: "POST",
            url: "/accounts/auth-token/",
            data: JSON.stringify(credentials),
            success: function (auth) {
                $.ajax({
                    type: "GET",
                    url: "/accounts/restricted/",
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("Authorization", "JWT " + auth.token);
                    },
                    success: function (data) {
                        // usid = data.id
                        // setCookie("user", data.username + ',' + data.id, 300)
                        $('#login').modal('toggle')
                        // $("#myNavbar").empty()
                        // $("#myNavbar").append('<ul class="nav navbar-nav navbar-right"><li><a href="#" id="userpr"><i class="fa fa-user-circle-o color-green" aria-hidden="true"></i> Welcome ' + data.username + ' !</a></li><li><a href="#" id="logout"><i class="fa fa-sign-out color-green" aria-hidden="true"></i> Logout</a></li></ul>')
                        window.location='/tweet/home/';
                        // $(".text-dec").empty()
                        // $(".text-dec").append("Welcome to ToDo")
                    },
                });
            },
            error: function (jqXHR) {
                $("#log-body").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> Wrong Credentials.</div>')
            },
            dataType: "json",
            contentType: "application/json",
        });
    });
    $("form#registerForm").submit(function (e) {
        e.preventDefault();
        // var credentials = {}
        // credentials['email'] = $("#emailid").val()
        // credentials['username'] = $("#uname").val()
        // credentials['firstname'] = $("#fname").val()
        // credentials['lastname'] = $("#lname").val()
        // credentials['phone'] = $("#phone").val()
        // credentials['faculty'] = $("#faculty").val()
        // credentials['password'] = $("#pass").val()
        // credentials['dp'] = $('#profileimg').prop('files')[0];
        // credentials['confirm_password'] = $("#cfmpass").val()
        var aka=new FormData(this);
        $.ajax({
            type: "POST",
            url: "/accounts/register/",
            data: aka, //JSON.stringify(credentials),
            async: false,
            success: function (auth) {
                // $('#register').modal('toggle')
                $("body").prepend('<div id="regsucc" class="modal fade"><div class="modal-dialog"><div class="modal-content alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="modal" aria-label="close">×</a><strong>Congratulations!</strong> You have successfully Registered. Please Login to Continue.'+auth.faculty+'</div></div></div>')
                $("#regsucc").modal('show')
            },
            error: function (errors) {
                $("#reg-body").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> Already exists.</div>')
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
    });
});