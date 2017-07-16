// @Author: Javier Cienfuegos Jr
// @Title: createAccountValidation.js
// @Purpose: Validate entries before submit

/*
The following statements functions are event handlers for the
text boxes in order to detect any errors to the constraints imposed.
*/

$(document).ready(function () {
   $("#pwd").keyup(validPassword);
});

$(document).ready(function () {
    $("#pwd_check").keyup(validPasswordReenter);
});

$(document).ready(function () {
    $("#reg_email").keyup(function() {
        var re = new RegExp(/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/);
        if (re.test($('#reg_email').val()) && $.inArray($('#reg_email').val(), invalidEmails) == -1){
            if ($('#fg-email').hasClass('has-error')) {
                $('#fg-email').removeClass('has-error');
                $('#fg-email').children('span').remove();
            }

            if (!$('#fg-email').hasClass('has-success')) {
                $('#fg-email').addClass('has-success');
                $('#fg-email').append("<span class='glyphicon glyphicon-ok form-control-feedback'></span>");
            }

            if (!$('#fg-email').hasClass('has-feedback')) {
                $('#fg-email').addClass('has-feedback');
            }


        } else {
            if ($('#fg-email').hasClass('has-success')) {
                $('#fg-email').removeClass('has-success');
                $('#fg-email').children('span').remove();
            }

            if (!$('#fg-email').hasClass('has-error')) {
                $('#fg-email').addClass("has-error");
                $('#fg-email').append("<span class='glyphicon glyphicon-remove form-control-feedback'></span>");
            }

            if (!$('#fg-email').hasClass('has-feedback')) {
                $('#fg-email').addClass("has-feedback");
            }
        }
    });
});

validPassword = function() {
    var re = new RegExp(/^(?=.*[0-9])[a-zA-Z0-9!@#$%^&*]{6,30}$/);
    if (re.test($('#pwd').val())) {

        if ($('#fg-pwd').hasClass('has-error')) {
            $('#fg-pwd').removeClass('has-error');
            $('#fg-pwd').children('span').remove();
        }

        if (!$('#fg-pwd').hasClass('has-success')) {
            $('#fg-pwd').addClass('has-success');
            $('#fg-pwd').append("<span class='glyphicon glyphicon-ok form-control-feedback'></span>");
        }

        if (!$('#fg-pwd').hasClass('has-feedback')) {
            $('#fg-pwd').addClass('has-feedback');
        }
    } else {

        if ($('#fg-pwd').hasClass('has-success')) {
            $('#fg-pwd').removeClass('has-success');
            $('#fg-pwd').children('span').remove();
        }

        if (!$('#fg-pwd').hasClass('has-error')) {
            $('#fg-pwd').addClass("has-error");
            $('#fg-pwd').append("<span class='glyphicon glyphicon-remove form-control-feedback'></span>");
        }

        if (!$('#fg-pwd').hasClass('has-feedback')) {
            $('#fg-pwd').addClass("has-feedback");
        }

    }
}

validPasswordReenter = function() {
    if ($('#pwd').val() != $('#pwd_check').val()) {
        if ($('#fg-pwdcheck').hasClass('has-success')) {
            $('#fg-pwdcheck').removeClass('has-success');
            $('#fg-pwdcheck').children('span').remove();
        }

        if (!$('#fg-pwdcheck').hasClass('has-error')) {
            $('#fg-pwdcheck').addClass("has-error");
            $('#fg-pwdcheck').append("<span class='glyphicon glyphicon-remove form-control-feedback'></span>");
        }

        if (!$('#fg-pwdcheck').hasClass('has-feedback')) {
            $('#fg-pwdcheck').addClass("has-feedback");
        }
    } else {

        if ($('#fg-pwdcheck').hasClass('has-error')) {
            $('#fg-pwdcheck').removeClass('has-error');
            $('#fg-pwdcheck').children('span').remove();
        }

        if (!$('#fg-pwdcheck').hasClass('has-success')) {
            $('#fg-pwdcheck').addClass('has-success');
            $('#fg-pwdcheck').append("<span class='glyphicon glyphicon-ok form-control-feedback'></span>");
        }

        if (!$('#fg-pwdcheck').hasClass('has-feedback')) {
            $('#fg-pwdcheck').addClass('has-feedback');
        }
    }
}

function accountValidation() {
    var form_group_good = $('.form-group').each(function(i, obj) {
        if ($(this).hasClass('has-error')) {
            event.preventDefault();
            alert('Please the correct the highlighted information.');
            return false;
        }
    });
    return true;
}