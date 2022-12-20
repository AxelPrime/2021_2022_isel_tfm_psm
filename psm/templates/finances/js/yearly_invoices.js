'use strict'

let YearlyInvoices = function () {
    let invoiceDetailsTable = null;

    /**
     * Initialization function.
     */
    function init() {

    }

    /**
     * Function used to obtain the invoice data.
     */
    function getInvoiceData(elem) {
        const btn = $(elem)
        // Get the invoice id.
        const invoiceNumber = btn.attr('data-invoice-id')
        // Set the datatable.
        if (invoiceDetailsTable === null) {
            invoiceDetailsTable = $("#receipt_details").DataTable({
                columns: [
                    { title: 'Nome do Paciente' },
                    { title: 'Mês' },
                    { title: 'Inicio Contabilização' },
                    { title: 'Fim Contabilização' },
                    { title: 'Diárias' },
                    { title: 'Diárias (€)' },
                    { title: 'Detalhes' },
                ],
                "autoWidth": false,
                serverSide: true,
                ajax: {
                    url: '/api/financial/datatables/yearly-invoice/details',
                    type: 'GET',
                    'beforeSend': function (request) {
                        request.setRequestHeader("Authorization", `Token ${Cookies.get('userToken')}`);
                    },
                    data: (d) => {
                        d.invoice_number = invoiceNumber
                    }
                }
            })
        }
        invoiceDetailsTable.ajax.reload()
        // invoiceDetailsTable.columns.adjust().draw();

        $("#download_invoice_btn").attr('data-invoice-id', invoiceNumber)
        $("#receipt_details_modal").modal("show")
    }

    /**
     * Function used to download an invoice.
     */
    function downloadInvoice(elem) {
        const downloadBtn = $(elem)
        const invoiceNumber = downloadBtn.attr("data-invoice-id")

        fetch('/api/invoices/yearly-invoices/download/?invoice_number=' + invoiceNumber, {
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
            .catch(() => {
                return Swal.fire({
                    icon: 'error',
                    title: 'Ocorreu um erro',
                    text: "Ocorreu um erro. Por favor tente mais tarde."
                })
            });
    }

    return {
        init: init,
        getInvoiceData: getInvoiceData,
        downloadInvoice: downloadInvoice,
    }
}()

$(document).ready(function () {
    YearlyInvoices.init()
})