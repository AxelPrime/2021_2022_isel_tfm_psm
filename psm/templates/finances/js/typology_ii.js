'use strict'

let TypologyII = function () {
    let statsTable = null

    /**
     * Initialization function.
     */
    function init() {

    }

    /**
     * Function used to obtain the stats data.
     */
    function getStatsData(elem) {
        // Build the datatable is it does not exist.
        if (statsTable === null) {
             statsTable = $("#stats_details").DataTable({
                columns: [
                    { title: 'Nome da Instituição' },
                    { title: 'NIF' },
                    { title: 'Código' },
                    { title: 'Total Pacientes' },
                    { title: 'Diárias (€)' },
                ],
                "autoWidth": false,
            })
        }

        // Get the Button element.
        const btn = $(elem)

        // Prepare the request data.
        const reqData = {
            year: btn.attr('data-stats-year'),
            month: btn.attr('data-stats-month'),
        }
        // Make the request.
        $.ajax({
            url: '/api/stats/typology-ii/stats/',
            type: 'GET',
            data: reqData,
            headers: {
                "Authorization": `Token ${Cookies.get('userToken')}`
            },
            success: function (data) {
                const stats = data['data']['stats']
                // Clear the table data.
                statsTable.clear()
                // Add the new data to the table.
                statsTable.rows.add(stats).draw(false)
                // Add the month and year to the download button.
                $("#download_file_btn")
                    .attr("data-year", btn.attr('data-stats-year'))
                    .attr("data-month", btn.attr('data-stats-month'))

                // Show the modal.
                $("#stats_details_modal").modal('show')
            },
            error: function (jq) {
                GenericFunctions.errorHandler(jq.status, jq.responseText)
            }
        })
    }

    /**
     * Function used to download the file.
     */
    function downloadFile(elem) {
        const btn = $(elem)
        // Obtain the year.
        const year = btn.attr("data-year")
        // Obtain the month.
        const month = btn.attr("data-month")

        // Define the URL.
        const url = `/api/stats/typology-ii/stats/download/?year=${year}&month=${month}`
        // Download the file.
        fetch(url, {
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

    /**
     * Public functions
     */
    return {
        init: init,
        getStatsData: getStatsData,
        downloadFile: downloadFile
    }
}()

$(document).ready(function () {
    TypologyII.init()
})