'use strict'

let Referrals = function() {
    let canCreate = false

    /**
     * Initialization function.
     */
    function init() {
        // Set the datepicker format.
        $("#patient_birth_date").datepicker({
            format: "dd/mm/yyyy"
        })
        // Set the listener for submit.
        submitReferral()
        // Set to evaluate selector.
        evaluationSelector()
    }

    /**
     * Allow the search for a patient's data.
     */
    function searchPatient(elem) {
        // Get the JQuery Element.
        const searchBtn = $(elem)
        // Activate the spinner.
        GenericFunctions.toggleSpinner(searchBtn, true)
        // Obtain the patient's SNS Number.
        const snsNumber = $("#patient_sns_number").val()
        // Validate if the SNS is filled.
        if (!snsNumber){
            GenericFunctions.toggleSpinner(searchBtn, false)
            $("#sns_warning_text").text('É necessário preencher este campo!').removeClass('d-none')
            return
        }

        // Make the AJAX request.
        $.ajax({
            url: '/api/referrals/patient-data/',
            type: 'GET',
            data: {
                'sns_number': snsNumber
            },
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`
            },
            success: function (data) {
                canCreate = false
                const patientData = data['data']['patient']
                $("#patient_social_security_number").val(patientData['social_sec_number'])
                $("#patient_full_name").val(patientData['name'])
                $("#patient_phone_number").val(patientData['phone_number'])
                $("#patient_birth_date").val(patientData['birth_date'])
                $("#patient_address").val(patientData['address'])
                $("#patient_postal_code").val(patientData['postal_code'])
                $("#patient_locality").val(patientData['locality'])
                $("#patient_country").val(patientData["country"])
                $("#patient_nationality").val(patientData["nationality"])
                $("#patient_gender").val(patientData["gender"])
                $(`#patient_subsystem option[value="${patientData["subsystem"]}"]`).prop('selected', true)
                GenericFunctions.toggleSpinner(searchBtn, false)
                $("#sns_warning_text").addClass('d-none')
            },
            error: function (jq) {
                canCreate = true
                let message = 'Erro ao obter dados do paciente!'
                if (jq.status !== 500) {
                    let responseJson = JSON.parse(jq.responseText)
                    message = responseJson['message']
                }
                $("#sns_warning_text").text(message).removeClass('d-none')
                GenericFunctions.toggleSpinner(searchBtn, false)
            }
        })
    }

    /**
     * Function used to make the referral creation request.
     */
    function createReferral(createInDb, submitButton) {
        // Obtain the form.
        let form = $("#refer_patient_form")
        let validForm = form[0].checkValidity()
        form.addClass('was-validated')
        if (!validForm) {
            GenericFunctions.toggleSpinner(submitButton, false)
            return
        }

        // Create the form data.
        let formData = new FormData()
        // Add the data to submit from the form.
        formData.append("patient_name", $("#patient_full_name").val())
        formData.append("patient_sns_number", $("#patient_sns_number").val())
        formData.append("patient_social_security_number", $("#patient_social_security_number").val())
        formData.append("patient_phone_number", $("#patient_phone_number").val())

        formData.append("patient_gender", $("#patient_gender").val())
        formData.append("patient_country", $("#patient_country").val())
        formData.append("patient_nationality", $("#patient_nationality").val())


        formData.append("patient_birth_date", $("#patient_birth_date").val())
        formData.append("patient_disease_type", $("#patient_disease_type").val())
        formData.append("patient_admission_diagnosis", $("#patient_admission_diagnosis").val())
        formData.append("patient_internment_duration", $("#patient_internment_duration").val())

        formData.append("patient_next_of_kin_name", $("#patient_next_of_kin_name").val())
        formData.append("patient_next_of_kin_kinship", $("#patient_next_of_kin_kinship").val())
        formData.append("patient_next_of_kin_contact", $("#patient_next_of_kin_contact").val())

        formData.append("patient_internment_motive", $("#patient_internment_motive").val())

        formData.append("patient_other_diagnosis", $("#patient_other_diagnosis").val())
        formData.append("patient_medication", $("#patient_medication").val())

        formData.append("patient_supervision", $("#patient_supervision").val())
        formData.append("patient_social_security_status", $("#patient_social_security_status").val())
        formData.append("patient_social_status", $("#patient_social_status").val())

        formData.append("patient_origin_institution", $("#patient_origin_institution").val())
        formData.append("patient_care_house", $("#patient_care_house").val())

        formData.append("patient_address", $("#patient_address").val())
        formData.append("patient_postal_code", $("#patient_postal_code").val())
        formData.append("patient_locality", $("#patient_locality").val())

        formData.append("patient_doctor_name", $("#patient_doctor_name") ? $("#patient_doctor_name").val() : '')
        formData.append("patient_doctor_professional_certificate", $("#patient_doctor_professional_certificate") ? $("#patient_doctor_professional_certificate").val() : '')

        formData.append("patient_social_assistant", $("#patient_social_assistant").val())
        formData.append("patient_subsystem", $("#patient_subsystem").val())

        formData.append("patient_responsibility_term", $("#patient_responsibility_term")[0].files[0])
        formData.append("patient_supervision_scale", $("#patient_supervision_scale")[0].files[0])

        formData.append("create_db", createInDb)

        // Send the data to the server.
        $.ajax({
            url: '/api/referrals/refer-patient/',
            type: 'POST',
            contentType: false,
            processData: false,
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`
            },
            data: formData,
            success: function (data) {
                GenericFunctions.toggleSpinner(submitButton, false)
                $("#refer_patient_modal").modal('hide')
                Swal.fire({
                    icon: 'success',
                    title: 'Referenciação Criada!',
                    text: 'Referenciação criada com sucesso',
                })
                    .then(() => {
                        form.removeClass('was-validated')
                        form[0].reset()
                        referralsTable.ajax.reload()
                    })
            },
            error: function (jq) {
                $("#refer_patient_modal").modal('hide')
                GenericFunctions.errorHandler(jq.status, jq.responseText, submitButton)
            }
        })
    }

    /**
     * Function to handle the submission of the referral.
     */
    function submitReferral() {
        // Obtain the submit button elem.
        const submitButton = $("#refer_patient_submit")
        // On-click function for submit button.
        submitButton.on('click', function (ev) {
            ev.preventDefault()
            // Activate the spinner.
            GenericFunctions.toggleSpinner(submitButton, true)

            if (canCreate) {
                Swal.fire({
                    title: 'Pretende guardar os dados do paciente no sistema Hosix?',
                    text: "Ao clicar 'Sim', os dados introduzidos serão armazenados para utilização no futuro.",
                    showDenyButton: true,
                    confirmButtonText: 'Sim',
                    denyButtonText: `Não`,
                    allowOutsideClick: false,
                    icon: "question"
                }).then((result) => {
                    let createInDb = result.isConfirmed
                    createReferral(createInDb, submitButton)
                })
            } else {
                createReferral(false, submitButton)
            }

        })
    }

    /**
     * Obtain the details of a referral.
     */
    function getReferralDetails(elem) {
        // Obtain the referral ID.
        let referralId = $(elem).attr('data-referral-id')
        // Make the request.
        $.ajax({
            url: '/api/referrals/details/',
            type: 'GET',
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`
            },
            data: {
                'referral_id': referralId
            },
            success: function (data) {
                // Obtain the response data.
                let referralData = data['data']['referral_data']
                let html = `
                    <div class="row form-group mb-3">
                        <div class="col-3">
                            <label>Nº SNS</label>
                            <div type="text" class="form-control">${referralData['patient_sns_number']}</div>
                        </div>
                        <div class="col-3">
                            <label for="patient_social_security_number">Nº Seg. Social</label>
                            <div type="text" class="form-control">${referralData['patient_social_security_number']}</div>
                        </div>
                        <div class="col-4">
                            <label for="patient_full_name">Nome Completo</label>
                            <div type="text" class="form-control">${referralData['patient_name']}</div>
                        </div>
                        <div class="col-2">
                            <label for="patient_phone_number">Contacto Telefónico</label>
                            <div type="text" class="form-control">${referralData['patient_phone_number']}</div>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-3">
                            <label for="patient_birth_date">Data de Nascimento</label>
                            <div type="text" class="form-control">${referralData['patient_birth_date']}</div>
                        </div>
                        <div class="col-3">
                            <label for="patient_disease_type">Tipo de Doença</label>
                            <div type="text" class="form-control">${referralData['disease_type']}</div>
                        </div>
                        <div class="col-3">
                            <label for="patient_admission_diagnosis">Diagonóstico de Admissão (CID10)</label>
                            <div type="text" class="form-control">${referralData['admission_diagnosis']}</div>
                        </div>
                        <div class="col-3">
                            <label for="patient_internment_duration">Duração do Internamento</label>
                            <div type="text" class="form-control">${referralData['internment_duration']}</div>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-6">
                            <label for="patient_next_of_kin_name">Nome do Parente</label>
                            <div type="text" class="form-control">${referralData['relative_name']}</div>
                        </div>
                        <div class="col-3">
                            <label for="patient_next_of_kin_kinship">Grau de Parentesco</label>
                            <div type="text" class="form-control">${referralData['relative_kinship']}</div>
                        </div>
                        <div class="col-3">
                            <label for="patient_next_of_kin_contact">Contacto do Parente</label>
                            <div type="text" class="form-control">${referralData['relative_contact']}</div>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-12">
                            <label>Motivo de Internamento</label>
                            <textarea type="text" readonly class="form-control" rows="5" style="resize: none">${referralData['referral_motive']}</textarea>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-6">
                            <label for="patient_other_diagnosis">Outros Diagonósticos Não Pesquiátricos</label>
                            <textarea type="text" class="form-control" readonly rows="5" style="resize: none">${referralData['other_diagnosis']}</textarea>
                        </div>
                        <div class="col-6">
                            <label for="patient_medication">Medicação (Psiquiátrica/Não Psiquiátrica)</label>
                            <textarea type="text" class="form-control" readonly rows="5" style="resize: none">${referralData['medication']}</textarea>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-4">
                            <label for="patient_supervision">Supervisão</label>
                            <div type="text" class="form-control">${referralData['supervision_grade']}</div>
                        </div>
                        <div class="col-4">
                            <label for="patient_social_security_status">Situação Segurança Social</label>
                            <div type="text" class="form-control">${referralData['social_situation']}</div>
                        </div>
                        <div class="col-4">
                            <label for="patient_social_status">Estado Social</label>
                            <div type="text" class="form-control">${referralData['family_situation']}</div>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-3">
                            <label for="patient_origin_institution">Instituição de Origem</label>
                            <div type="text" class="form-control">${referralData['origin_institution_name']}</div>
                        </div>
                        <div class="col-3">
                            <label for="patient_care_house">Casa de Saude Destino</label>
                            <div type="text" class="form-control">${referralData['care_house_name']}</div>
                        </div>
                        <div class="col-6">
                            <label for="patient_address">Local de Residência</label>
                            <div type="text" class="form-control">${referralData['patient_address']}</div>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-6">
                            <label for="patient_address">Código Postal</label>
                            <div type="text" class="form-control">${referralData['patient_postal_code']}</div>
                        </div>
                        <div class="col-6">
                            <label for="patient_address">Localidade</label>
                            <div type="text" class="form-control">${referralData['patient_locality']}</div>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-6">
                            <label for="patient_social_assistant">Assistente Social</label>
                            <div type="text" class="form-control">${referralData['social_assistant']}</div>
                        </div>
                        <div class="col-6">
                            <label for="patient_subsystem">Subsistema de Saúde</label>
                            <div type="text" class="form-control">${referralData['patient_subsystem']}</div>
                        </div>
                    </div>
                    <div class="row form-group mb-3">
                        <div class="col-6 d-flex justify-content-center">
                            <button type="button" class="btn btn-primary" onclick="GenericFunctions.downloadResponsibilityTerm('${referralId}')">Transferir Termo de Responsabilidade</button>
                        </div>
                        <div class="col-6 d-flex justify-content-center">
                            <button type="button" class="btn btn-primary" onclick="GenericFunctions.downloadSupervisionScale('${referralId}')">Transferir Escala de Supervisão</button>
                        </div>
                    </div>
                `
                const detailsModal = $("#referrals_details_modal")
                detailsModal.find('.modal-body').html(html)
                detailsModal.modal('show')
            },
            error: function (jq) {
                GenericFunctions.errorHandler(jq.status, jq.responseText)
            }
        })
    }

    /**
     * Evaluate a set of referrals.
     */
    function evaluateReferrals() {
        let nextStatus = $("#evaluation").val()
        let rejectionReason = $("#rejection_reason").val()
        $("#evaluate_referral_modal").modal('hide')

        let checkedData = []
        $("#pending_referrals_body tr td input:checkbox").each(function () {
            if (this.checked) checkedData.push($(this).attr('data-referral-id'))
        })

        Swal.fire({
            title: 'Tem a certeza? ',
            text: `Irá alterar o estado de ${checkedData.length} referenciações. Não poderá voltar atrás.`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Confirmar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                const requestData = {
                    status: nextStatus,
                    referrals: checkedData,
                    rejection_reason: rejectionReason
                }

                $.ajax({
                    url: '/api/referrals/evaluate/',
                    type: 'POST',
                    headers: {
                        'content-type': 'application/json',
                        'Authorization': `Token ${Cookies.get('userToken')}`,
                    },
                    data: JSON.stringify(requestData),
                    success: function (data) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Referenciações Avaliadas!',
                            text: 'Referenciação avaliadas com sucesso',
                        })
                            .then(() => {
                                Notifications.getNotifications()
                                referralsTable.ajax.reload()
                            })
                    },
                    error: function (jq) {
                        GenericFunctions.errorHandler(jq.status, jq.responseText)
                    }
                })
            }
        })
    }

    /**
     * Show the rejection reason depending on the selected value.
     */
    function evaluationSelector() {
        let evaluation = $("#evaluation")
        evaluation.on('change', function (ev) {
            ev.preventDefault()
            let rejectionReason = $("#rejection_reason_div")
            evaluation.val() === 'referral_rejected' ? rejectionReason.removeClass('d-none') : rejectionReason.addClass('d-none')
        })
    }

    return {
        init: init,
        getReferralDetails: getReferralDetails,
        evaluateReferrals: evaluateReferrals,
        searchPatient: searchPatient
    }
}()


$(document).ready(function () {
    Referrals.init()
})