var glbl, usid
var itup
function list_disp() {
    $.ajax({
        type: "GET",
        url: "/todo/lists/",
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
function item_disp(key) {
    $.ajax({
        type: "GET",
        url: "/todo/list/" + key + "/",
        success: function (data) {
            if (data.length == 0) {
                $('#row-main').empty()
                $('#header-section').empty()
                $('#header-section').append('<h2>ToDo Items</h2><hr class="bottom-line"><button id="itemnew" class="btn btn-success btn-sm"><i class="fa fa-list fa-fw"></i> New Item</button>')
                $('#row-main').append('<div class="alert alert-info">No Items to display.</div>')
            }
            else {
                $.get('/static/itemsf.html', function (htm) {
                    $('#row-main').empty()
                    $('#header-section').empty()
                    $('#header-section').append('<h2>ToDo Items</h2><hr class="bottom-line"><button id="itemnew" class="btn btn-success btn-sm"><i class="fa fa-list fa-fw"></i> New Item</button>')
                    $.tmpl(htm, data).appendTo("#row-main")
                });
            }
        },
    });
}
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
function setCookie(cname, cvalue, exsec) {
    var d = new Date();
    d.setTime(d.getTime() + (exsec * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function checkCookie() {
    var username = getCookie("user");
    if (username != "") {
        username = username.split(',')
        usid = username[1]
        $("#myNavbar").empty()
        $("#myNavbar").append('<ul class="nav navbar-nav navbar-right"><li><a href="#" id="userpr"><i class="fa fa-user-circle-o color-green" aria-hidden="true"></i> Welcome ' + username[0] + ' !</a></li><li><a href="#" id="logout"><i class="fa fa-sign-out color-green" aria-hidden="true"></i> Logout</a></li></ul>')
        list_disp()
        $(".text-dec").empty()
        $(".text-dec").append("Welcome to ToDo")
    }
}
$("document").ready(function () {
    checkCookie();
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
                        usid = data.id
                        setCookie("user", data.username + ',' + data.id, 300)
                        $('#login').modal('toggle')
                        $("#myNavbar").empty()
                        $("#myNavbar").append('<ul class="nav navbar-nav navbar-right"><li><a href="#" id="userpr"><i class="fa fa-user-circle-o color-green" aria-hidden="true"></i> Welcome ' + data.username + ' !</a></li><li><a href="#" id="logout"><i class="fa fa-sign-out color-green" aria-hidden="true"></i> Logout</a></li></ul>')
                        list_disp()
                        $(".text-dec").empty()
                        $(".text-dec").append("Welcome to ToDo")
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
    $("body").on('submit', '#registerForm', function (e) {
        e.preventDefault()
        var credentials = {}
        credentials['email'] = $("#emailid").val()
        credentials['username'] = $("#username").val()
        credentials['firstname'] = $("#firstname").val()
        credentials['lastname'] = $("#lastname").val()
        credentials['password'] = $("#password").val()
        credentials['confirm_password'] = $("#logincfmpsw").val()
        $.ajax({
            type: "POST",
            url: "/accounts/register/",
            data: JSON.stringify(credentials),
            success: function (auth) {
                $('#register').modal('toggle')
                $("body").prepend('<div id="myModal" class="modal fade"><div class="modal-dialog"><div class="modal-content alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="modal" aria-label="close">×</a><strong>Congratulations!</strong> You have successfully Registered. Please Login to Continue.</div></div></div>')
                $("#myModal").modal('show')
            },
            error: function (errors) {
                $("#reg-body").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> Already exists.</div>')
            },
            dataType: "json",
            contentType: "application/json",
        });
    });
    $("body").on("click", "a[id='home']", function (e) {
        e.preventDefault()
        var username = getCookie("user");
        if (username != "") {
            list_disp()
        }
    });
    $("body").on("click", "a[id='userpr']", function (e) {
        e.preventDefault()
        console.log(usid)
        $.ajax({
            type: "GET",
            url: "/accounts/profile/" + usid + "/",
            success: function (data) {
                $.get('/static/userprof.html', function (htm) {
                    $('#header-section').empty()
                    $('#header-section').append('<h2>Update Profile</h2><hr class="bottom-line">')
                    $("#row-main").empty()
                    $.tmpl(htm, data).prependTo("#row-main")
                });
            },
        });
    });
    $("#work-shop").on("submit", ".userprof", function (e) {
        e.preventDefault()
        var credentials = {}
        credentials['email'] = $("#emailidu").val()
        credentials['username'] = $("#usernameu").val()
        credentials['firstname'] = $("#firstnameu").val()
        credentials['lastname'] = $("#lastnameu").val()
        credentials['password'] = $("#passwordu").val()
        credentials['confirm_password'] = $("#logincfmpswu").val()
        $.ajax({
            type: "PUT",
            url: "/accounts/profile/" + usid + "/",
            data: credentials,
            success: function (data) {
                list_disp()
                $("#row-main").prepend('<div class="alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Success!</strong> Your Profile has been Successfully Updated.</div>')
            },
            error: function () {
                list_disp()
                $("#row-main").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> Your Profile cannot be Updated.</div>')
            }
        });
    });
    $("body").on("click", "a[id='logout']", function () {
        $.ajax({
            type: "GET",
            url: "/accounts/logout/",
            success: function (data) {
                $(location).attr('href', '/accounts/login/');
            },
        });
    });
    $("#work-shop").on("click", "button[id='listnew']", function () {
        $.get('/static/listnewf.html', function (htm) {
            $('#header-section').empty()
            $('#header-section').append('<h2>New ToDo List</h2><hr class="bottom-line">')
            $("#row-main").empty()
            $.tmpl(htm).prependTo("#row-main")
        });
    });
    $("#work-shop").on("click", "button[id='itemnew']", function () {
        $.get('/static/itemnewf.html', function (htm) {
            $('#header-section').empty()
            $('#header-section').append('<h2>Update ToDo Item</h2><hr class="bottom-line">')
            $("#row-main").empty()
            $.tmpl(htm).prependTo("#row-main")
        });
    });
    $("#work-shop").on("submit", ".lisup", function (e) {
        e.preventDefault()
        var credentials = {}
        credentials['name'] = $("#name").val()
        $.ajax({
            type: "PUT",
            url: "/todo/listup/" + glbl[2] + "/",
            data: credentials,
            success: function (data) {
                list_disp()
                $("#row-main").prepend('<div class="alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Success!</strong> The List has been Successfully Updated.</div>')
            },
            error: function () {
                list_disp()
                $("#row-main").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> This List cannot be Updated.</div>')
            }
        });
    });
    $("#work-shop").on("submit", ".itmup", function (e) {
        e.preventDefault()
        var credentials = {}
        credentials['descrip'] = $("#descrip").val()
        credentials['due_by'] = $("#due_by").val()
        credentials['list'] = itup
        $.ajax({
            type: "PUT",
            url: "/todo/itemup/" + glbl[2] + "/",
            data: credentials,
            success: function (data) {
                item_disp(itup)
                $("#row-main").prepend('<div class="alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Success!</strong> The Item has been Successfully Updated.</div>')
            },
            error: function () {
                item_disp(itup)
                $("#row-main").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> This Item cannot be Updated.</div>')
            }
        });
    });
    $("#work-shop").on("submit", ".lisnw", function (e) {
        e.preventDefault()
        var credentials = {}
        credentials['name'] = $("#name").val()
        $.ajax({
            type: "POST",
            url: "/todo/newlist/",
            data: credentials,
            success: function (data) {
                list_disp()
            },
        });
    });
    $("#work-shop").on("submit", ".itmnw", function (e) {
        e.preventDefault()
        var credentials = {}
        credentials['descrip'] = $("#descrip").val()
        credentials['due_by'] = $("#due_by").val()
        $.ajax({
            type: "POST",
            url: "/todo/newitem/" + itup + "/",
            data: credentials,
            success: function (data) {
                item_disp(itup)
            },
        });
    });
    $("#row-main").on("click", "button[name='btnn']", function (e) {
        e.preventDefault()
        var choice = $(this).attr('id');
        var akar = choice.split('_');
        glbl = akar
        if (akar[0] == 'list') {
            itup = akar[2]
            if (akar[1] == 'show') {
                item_disp(akar[2])
            }
            else if (akar[1] == 'update') {
                $.ajax({
                    type: "GET",
                    url: "/todo/listup/" + akar[2] + "/",
                    success: function (data) {
                        $.get('/static/listupf.html', function (htm) {
                            $('#header-section').empty()
                            $('#header-section').append('<h2>Update ToDo List</h2><hr class="bottom-line">')
                            $("#row-main").empty()
                            $.tmpl(htm, data).prependTo("#row-main")
                        });
                    },
                });
            }
            else if (akar[1] == 'delete') {
                $.ajax({
                    type: "DELETE",
                    url: "/todo/listup/" + akar[2] + "/",
                    success: function (data) {
                        list_disp()
                        $("#row-main").prepend('<div class="alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Success!</strong> The List has been Successfully Removed.</div>')
                    },
                    error: function () {
                        list_disp()
                        $("#row-main").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> This List cannot be Removed.</div>')
                    }
                });
            }
        }
        else if (akar[0] == 'item') {
            if (akar[1] == 'compltd') {
                $.ajax({
                    type: "GET",
                    url: "/todo/itemupd/" + akar[2] + "/",
                    success: function (data) {
                        item_disp(itup)
                        $("#row-main").prepend('<div class="alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Success!</strong> The Item has been Successfully Updated.</div>')
                    },
                    error: function () {
                        item_disp(itup)
                        $("#row-main").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> This Item cannot be Updated.</div>')
                    }
                });
            }
            if (akar[1] == 'update') {
                $.ajax({
                    type: "GET",
                    url: "/todo/itemup/" + akar[2] + "/",
                    success: function (data) {
                        $.get('/static/itemupf.html', function (htm) {
                            $('#header-section').empty()
                            $('#header-section').append('<h2>Update ToDo Item</h2><hr class="bottom-line">')
                            $("#row-main").empty()
                            $.tmpl(htm, data).prependTo("#row-main")
                        });
                    },
                });
            }
            else if (akar[1] == 'delete') {
                $.ajax({
                    type: "DELETE",
                    url: "/todo/itemup/" + akar[2] + "/",
                    success: function (data) {
                        item_disp(itup)
                        $("#row-main").prepend('<div class="alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Success!</strong> The Item has been Successfully Removed.</div>')
                    },
                    error: function () {
                        item_disp(itup)
                        $("#row-main").prepend('<div class="alert alert-error alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a><strong>Error!</strong> This Item cannot be Removed.</div>')
                    }
                });
            }
        }
    });
});
