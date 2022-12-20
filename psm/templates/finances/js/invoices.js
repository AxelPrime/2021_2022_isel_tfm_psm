'use strict'

let Invoices = function () {
    let invoiceData;

    /**
     * The initialization function.
     */
    function init() {
        setInvoiceCreationData()
        superuserVerifyInvoices()
        evaluationSelector()
    }

    /**
     * Function to set the invoice creation data.
     */
    function setInvoiceCreationData() {
        // Set the data.
        invoiceData = JSON.parse($("#next_invoices")[0].textContent)

        // Obtain the typology selector.
        const typologySelect = $("#typology_select")
        // Set the on change data.
        typologySelect.on('change', function() {
            // Declare the HTML body variable.
            let htmlBody = ''
            // Set the default footer html
            let footerHtml = `
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
                    Fechar
                </button>
            `
            // Obtain the next invoice data body.
            const nextInvoiceBody = $("#next_invoice_body")
            // Obtain the footer to set the buttons.
            const nextInvoiceFooter = $("#next_invoice_footer")
            // Obtain the current value of the selector.
            const selectedValue = typologySelect.val()
            // Check if the value is set.
            if (!selectedValue) {
                nextInvoiceBody.html(htmlBody)
                nextInvoiceFooter.html(footerHtml)
                return
            }

            // Obtain the data for the selected value.
            const data = invoiceData[selectedValue]
            // Build the body.
            if (data['can_create']) {
                htmlBody = `
                    <div class="row">
                        <div class="col-6">
                            <label class="form-label">Data de Inicio da Contabilização:</label>
                            <div class="form-control">${data["start_date"]}</div>
                        </div>
                        <div class="col-6">
                            <label class="form-label">Data de Fim da Contabilização:</label>
                            <div class="form-control">${data["end_date"]}</div>
                        </div>
                    </div>
                `

                footerHtml = `
                    <button type="button" id="create_invoice" class="btn btn-light-primary" data-typology="${selectedValue}" onclick="Invoices.createInvoice(this)">
                        <span class="indicator-progress d-none">
                            Aguarde...<span class="ms-2 spinner-border spinner-border-sm"></span>
                        </span>
                        <span class="indicator-label">Criar Listagem</span>
                    </button>
                `
            }
            else {
                htmlBody = `
                    <div class="fs-6">
                        ${data["message"]}
                    </div>
                `
                footerHtml = `
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
                        Fechar
                    </button>
                `
            }

            nextInvoiceBody.html(htmlBody)
            nextInvoiceFooter.html(footerHtml)
        })
    }

    /**
     * Function used for superuser to verify invoice dates.
     */
    function superuserVerifyInvoices() {
        // Obtain the care_house selector.
        const careHouseSelect = $("#care_house_select")
        // Verify if the care house select exists.
        if (!careHouseSelect[0]) return

        // Set the onchange.
        careHouseSelect.on('change', () => {
            // Obtain the typology select element.
            const typologySelect = $("#typology_select")
            // Obtain the value.
            let selectedValue = careHouseSelect.val()
            // Show the typology selete or hide it.
            if (!selectedValue) {
                typologySelect.val('').change()
                typologySelect.parent().addClass('d-none')
            }
            else {
                $.ajax({
                    url: "/api/invoices/monthly-invoices/superuser-verify/",
                    type: 'GET',
                    data: {
                        'care_house': selectedValue
                    },
                    headers: {
                        'Authorization': `Token ${Cookies.get('userToken')}`,
                    },
                    success: data => {
                        // Obtain the next invoice dates.
                        invoiceData = data['data']['next_invoices']
                        // Show the typology select.
                        typologySelect.val('').change()
                        typologySelect.parent().removeClass('d-none')
                    },
                    error: jq => {
                        GenericFunctions.errorHandler(jq.status, jq.responseText)
                    }
                })
            }
        })
    }

    /**
     * Handler function to create an invoice.
     */
    function createInvoice(elem) {
        const createInvoiceBtn = $(elem)
        GenericFunctions.toggleSpinner(createInvoiceBtn, true)
        // Create the request body.
        const requestBody = {
            typology: createInvoiceBtn.attr('data-typology'),
            care_house: $("#care_house_select").val()
        }
        // Make the request.
        $.ajax({
            url: '/api/invoices/monthly-invoices/create/',
            type: 'POST',
            data: JSON.stringify(requestBody),
            headers: {
                'content-type': 'application/json',
                'Authorization': `Token ${Cookies.get('userToken')}`,
            },
            success: function (data) {
                Notifications.getNotifications()
                window.location.reload()
            },
            error: function (jq) {
                GenericFunctions.errorHandler(jq.status, jq.responseText, createInvoiceBtn)
            }
        })
    }

    /**
     * Function to display the invoice details.
     */
    function getInvoiceDetails(elem) {
        const invoiceDetailsBtn = $(elem)
        // Prepare the request.
        const reqBody = {
            'invoice_number': invoiceDetailsBtn.attr("data-invoice-id")
        }
        // Make the request.
        $.ajax({
            url: '/api/invoices/monthly-invoices/details/',
            type: 'GET',
            data: reqBody,
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`,
            },
            success: function (data) {
                // Obtain the invoice lines.
                const invoice_lines = data['data']['invoice_lines']

                // Clear the current DataTable's rows.
                receiptDetailsTable.clear()
                receiptDetailsTable.rows.add(invoice_lines).draw()
                $("#invoice_details_title").text(`Listagem de ${data['data']['month']} de ${data['data']['year']}`)
                let footerHtml = ''
                if (data['data']['is_final']) {
                    footerHtml = `
                        <button type="button" class="btn btn-primary" onclick="Invoices.downloadInvoicePdf('${reqBody.invoice_number}')">Download Recibo</button>
                    `
                } else {
                    $("#finalize_invoice_submit").attr('data-invoice-number', reqBody.invoice_number)
                    footerHtml = `
                        <button type="button" class="btn btn-primary" data-bs-target="#finalize_invoice_modal" data-bs-toggle="modal" data-bs-dismiss="modal">Finalizar Listagem</button>
                    `
                }
                const modalFooter = $("#invoice_details_footer")
                if (modalFooter.attr('data-can-evaluate') === 'true') {
                    $("#evaluate_invoice_submit").attr('data-invoice-number', reqBody.invoice_number)
                    footerHtml += `
                        <button type="button" class="btn btn-primary" data-bs-target="#evaluate_invoice_modal" data-bs-toggle="modal" data-bs-dismiss="modal">Avaliar Listagem</button>
                    `
                }
                modalFooter.html(footerHtml)

                $("#receipt_details_modal").modal('show')
            },
            error: function (jq) {
                GenericFunctions.errorHandler(jq.status, jq.responseText)
            }
        })
    }

    /**
     * Funtion used to download the invoice PDF.
     */
    function downloadInvoicePdf(invoiceNumber) {
        fetch('/api/invoices/monthly-invoices/download/?invoice_number=' + invoiceNumber, {
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
     * Function used for the evaluation selector.
     */
    function evaluationSelector() {
        const selector = $("#approve_select")
        selector.on('change', () => {
            const rejectionReasonDiv = $("#rejection_reason_div")
            selector.val() === 'false' ? rejectionReasonDiv.removeClass('d-none') : rejectionReasonDiv.addClass('d-none')
        })
    }

    /**
     * Function used to finalize an invoice
     */
    function finalizeInvoice(elem) {
        const submitBtn = $(elem)
        // Obtain the invoice number.
        const invoiceNumber = submitBtn.attr('data-invoice-number')
        // Activate the spinner for the button.
        GenericFunctions.toggleSpinner(submitBtn, true)
        // Prepare the form data.
        const formData = new FormData()
        // Add the data.
        formData.append('invoice_number', invoiceNumber)
        formData.append('invoice_file', $("#invoice_file")[0].files[0])

        // Make the request.
        $.ajax({
            url: '/api/invoices/monthly-invoices/finalize/',
            type: 'POST',
            contentType: false,
            processData: false,
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`
            },
            data: formData,
            success: function (data) {
                Notifications.getNotifications()
                window.location.reload()
            },
            error: function (jq) {
                GenericFunctions.errorHandler(jq.status, jq.responseText, submitBtn)
            }
        })
    }

    /**
     * Function used to evaluate the invoice.
     */
    function evaluateInvoice(elem) {
        const submitBtn = $(elem)
        // Obtain the invoice number.
        const invoiceNumber = submitBtn.attr('data-invoice-number')
        // Activate the spinner for the button.
        GenericFunctions.toggleSpinner(submitBtn, true)
        // Prepare the request body.
        const reqBody = {
            invoice_number: invoiceNumber,
            approve: $("#approve_select").val(),
            rejection_reason: $("#rejection_reason").val()
        }
        // Make the request.
        $.ajax({
            url: '/api/invoices/monthly-invoices/evaluate/',
            type: 'POST',
            data: JSON.stringify(reqBody),
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`,
                'Content-Type': 'application/json'
            },
            success: data => {
                Notifications.getNotifications()
                window.location.reload()
            },
            error: jq => {
                GenericFunctions.errorHandler(jq.status, jq.responseText, submitBtn)
            }
        })
    }

    return {
        init: init,
        createInvoice: createInvoice,
        getInvoiceDetails: getInvoiceDetails,
        downloadInvoicePdf: downloadInvoicePdf,
        finalizeInvoice: finalizeInvoice,
        evaluateInvoice: evaluateInvoice,
    }
}()

$(document).ready(function () {
    Invoices.init()
})