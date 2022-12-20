'use strict'

let GenericFunctions = function () {
    /**
     * Initialization function
     */
    function init() {

    }

    /**
     * Toggle the spinner on a button.
     */
    function toggleSpinner(button, active) {
        if (active) {
            button.find('.indicator-progress').removeClass('d-none')
            button.find('.indicator-label').addClass('d-none')
        }
        else {
            button.find('.indicator-progress').addClass('d-none')
            button.find('.indicator-label').removeClass('d-none')
        }
    }

    /**
     * Handle errors on API response.
     */
    function errorHandler(statusCode, response, button=null) {
        let message = "Ocorreu um erro. Por favor tente mais tarde."
        if (statusCode !== 500) {
            message = JSON.parse(response)['message']
        }

        if (button !== null) {
            toggleSpinner(button, false)
        }

        Swal.fire({
          icon: 'error',
          title: 'Ocorreu um erro...',
          text: message
        })
    }

    /**
     * Logout function
     */
    function logout() {
        $.ajax({
            url: '/api/users/logout/',
            type: 'POST',
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`
            },
            success: function (data) {
                window.location.href = '/login/'
            },
            error: function (jq) {
                errorHandler(jq.status, jq.responseText)
            }
        })
    }

    /**
     * Handler for responsibility term download.
     */
    function downloadResponsibilityTerm(referralId) {
        fetch('/api/referrals/responsibility-term/?referral_id=' + referralId, {
                method: 'GET',
                headers: new Headers({
                    'Authorization': `Token ${Cookies.get('userToken')}`
                })
            })
            .then(response => {
                const filename = response.headers.get('Content-Disposition').split('filename=')[1];
                response.blob().then(blob => {
                    let url = window.URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    a.click();
                })
            })
            .catch(() => alert('oh no!'));
    }

        /**
     * Handler for responsibility term download.
     */
    function downloadSupervisionScale(referralId) {
        fetch('/api/referrals/supervision-scale/?referral_id=' + referralId, {
                method: 'GET',
                headers: new Headers({
                    'Authorization': `Token ${Cookies.get('userToken')}`
                })
            })
            .then(response => {
                const filename = response.headers.get('Content-Disposition').split('filename=')[1];
                response.blob().then(blob => {
                    let url = window.URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    a.click();
                })
            })
            .catch(() => alert('oh no!'));
    }

    return {
        init: init,
        toggleSpinner: toggleSpinner,
        errorHandler: errorHandler,
        logout: logout,
        downloadResponsibilityTerm: downloadResponsibilityTerm,
        downloadSupervisionScale: downloadSupervisionScale
    }
}()

$(document).ready(function () {
    GenericFunctions.init()
})