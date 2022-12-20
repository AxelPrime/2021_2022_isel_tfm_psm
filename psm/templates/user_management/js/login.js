'use strict'


let Login = function () {
    /** Initialization function. **/
    function init() {
        performLogin()
    }

    /** Perform the login. **/
    function performLogin() {
        $("#submit_login").on('click', function (ev) {
            ev.preventDefault()
            let requestData = {
                email: $("#email").val(),
                password: $("#password").val(),
                remember_user: $('#remember_user').is(":checked")
            }

            $.ajax({
                url: '/api/users/login/',
                type: 'POST',
                headers: {
                    'content-type': 'application/json'
                },
                data: JSON.stringify(requestData),
                success: function (data) {
                    window.location.href = data['data']['redirect_to']
                },
                error: function (jq) {
                    GenericFunctions.errorHandler(jq.status, jq.responseText)
                }
            })
        })
    }

    return {
        init: init
    }
}()

$(document).ready(function () {
    Login.init()
})