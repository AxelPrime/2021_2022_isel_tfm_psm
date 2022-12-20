'use strict'

let DailyValues = function() {
    /**
     * Initialization function.
     */
    function init() {
        // Set the datepicker format.
        $("#start_date").datepicker({
            format: "dd/mm/yyyy"
        })
    }

    /**
     * Function used to add a new daily value.
     */
    function addNewValue(elem) {
        // Obtain the element object.
        const button = $(elem)
        // Toggle the spinner.
        GenericFunctions.toggleSpinner(button, true)

        // Set the request body.
        const reqBody = {
            value: $("#new_value").val(),
            start_date: $("#start_date").val()
        }

        // Make the AJAX request.
        $.ajax({
            url: '/api/stats/daily-value/add/',
            type: 'POST',
            data: JSON.stringify(reqBody),
            headers: {
                'content-type': 'application/json',
                'Authorization': `Token ${Cookies.get('userToken')}`,
            },
            success: data => {
                window.location.reload()
            },
            error: (jq) => {
                GenericFunctions.errorHandler(jq.status, jq.responseText, button)
            }
        })
    }

    return {
        init: init,
        addNewValue: addNewValue
    }
}()

$(document).ready(() => {
    DailyValues.init()
})