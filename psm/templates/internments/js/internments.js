'use strict'

let Internments = function () {
    /**
     * Initialization function.
     */
    function init() {
        // Set the register handler.
        registerInternments()
        // Set submit handler.
        submitActivityLog()
    }

    /**
     * Function to register the internments in the care house.
     */
    function registerInternments() {
        // Obtain the register button element
        let registerBtn = $("#register_internments_btn")
        // Set the on click function.
        registerBtn.on('click', function (ev) {
            ev.preventDefault()
            // Set the register button as inactive.
            GenericFunctions.toggleSpinner(registerBtn, true)
            // Obtain the checked entries.
            let checkedData = []
            $("#pending_internments_body tr td input:checkbox").each(function () {
                if (this.checked) checkedData.push($(this).attr('data-referral-id'))
            })

            const requestData = {
                'referrals': checkedData
            }

            $.ajax({
                url: '/api/internments/register-internments/',
                type: 'POST',
                headers: {
                    'content-type': 'application/json',
                    'Authorization': `Token ${Cookies.get('userToken')}`,
                },
                data: JSON.stringify(requestData),
                success: function (data) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Internamentos Registados!',
                        text: 'Internamentos registados com sucesso',
                    })
                        .then(() => {
                            Notifications.getNotifications()
                            internmentsTable.ajax.reload()
                        })
                },
                error: function (jq) {
                    GenericFunctions.errorHandler(jq.status, jq.responseText)
                }
            })
        })
    }

    /**
     * Function to obtain the internment activity log.
     */
    function getActivityLog(elem) {
        // Get the JQuery element.
        const activityLogBtn = $(elem)
        // Get the internment ID.
        const internmentId = activityLogBtn.attr('data-internment-id')

        // Obtain the activity log.
        $.ajax({
            url: '/api/internments/activity-log/',
            type: 'GET',
            data: {
                internment_id: internmentId,
            },
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`,
            },
            success: function (data) {
                // Obtain the activity log.
                const activity = data['data']['logs']

                // Set the patient name.
                $("#activity_log_patient").text(data['data']['patient_name'])

                // Clear the current DataTable's rows.
                activityLogTable.clear().draw()

                // Add the rows to the table.
                activityLogTable.rows.add(activity).draw()

                const addActivityBtn = $("#add_activity_log_btn")

                // Set the next possible states.
                if (!data['data']['is_terminal']) {
                    addActivityBtn.removeClass('d-none')
                    // Set the activity type HTML.
                    let activityTypeHtml = `
                        <option value="">Selecione...</option>
                    `
                    data['data']['next_states'].forEach(val => {
                        activityTypeHtml += `
                            <option value="${val.label}">${val.name}</option>
                        `
                    })
                    $("#activity_type").html(activityTypeHtml)
                    $("#submit_activity_log_btn").attr('data-internment-id', internmentId)
                }
                else {
                    addActivityBtn.addClass('d-none')
                }

                // Open the modal.
                $("#activity_logs_modal").modal('show')
            },
            error: function (jq) {
                GenericFunctions.errorHandler(jq.status, jq.responseText)
            }
        })
    }

    /**.
     * Function to submit an activity log.
     */
    function submitActivityLog() {
        // Obtain the submit button.
        const submitBtn = $("#submit_activity_log_btn")
        // Check if the button exists.
        if (!submitBtn) return
        // Set the on click handler.
        submitBtn.on('click', function (ev) {
            ev.preventDefault()

            // Activate the spinner.
            GenericFunctions.toggleSpinner(submitBtn, true)

            // Obtain the form.
            let form = $("#add_activity_log_form")
            let validForm = form[0].checkValidity()
            form.addClass('was-validated')
            if (!validForm) {
                GenericFunctions.toggleSpinner(submitBtn, false)
                return
            }

            // Create the request data.
            const requestData = {
                next_state: $("#activity_type").val(),
                description: $("#activity_description").val(),
                internment_id: submitBtn.attr('data-internment-id')
            }

            // Make the request.
            $.ajax({
                url: '/api/internments/add-log/',
                type: 'POST',
                data: JSON.stringify(requestData),
                headers: {
                    'Authorization': `Token ${Cookies.get('userToken')}`,
                    'Content-Type': 'application/json'
                },
                success: function (data) {
                    GenericFunctions.toggleSpinner(submitBtn, false)
                    $("#add_activity_collapse").removeClass('show')
                    $("#activity_logs_modal").modal('hide')
                    Swal.fire({
                        icon: 'success',
                        title: 'Registo Criado!',
                        text: 'Registo de atividade criado com sucesso',
                    })
                        .then(() => {
                            form.removeClass('was-validated')
                            form[0].reset()
                            internmentsTable.ajax.reload()
                        })
                },
                error: function (jq) {
                    GenericFunctions.errorHandler(jq.status, jq.responseText, submitBtn)
                }
            })
        })
    }

    return {
        init: init,
        getActivityLog: getActivityLog,
    }
}()

$(document).ready(function () {
    Internments.init()
})