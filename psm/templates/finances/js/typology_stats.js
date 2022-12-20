'use strict'

let TypologyStats = function () {
    let typologyStatsTable = null
    let careHouseStatsTable = null

    /**
     * Initialization function.
     */
    function init() {

    }

    /**
     * Function used to open the typology stats modal.
     */
    function showTypologyStatsModal(elem) {
        const btn = $(elem)
        // Get the year to view.
        const year = btn.attr('data-year')
        // Get the modal to open.
        const modal = $("#typology_stats_modal")
        // Set the title.
        $("#typology_stats_modal_modal").text(`Dados de Tipologia - ${year}`)
        // Set the year.
        $("#typology_stats_search").attr('data-year', year)
        // Empty the table.
        $("#typology_stats_table").html('')
        // Add the year to the download button.
        $("#typology_stats_download_btn").attr('data-year', year)
        // Show the modal.
        modal.modal('show')
    }

    /**
     * Function used to open the typology stats modal.
     */
    function showCareHouseStatsModal(elem) {
        const btn = $(elem)
        // Get the year to view.
        const year = btn.attr('data-year')
        // Get the modal to open.
        const modal = $("#care_house_stats_modal")
        // Set the title.
        $("#care_house_stats_modal_modal").text(`Dados de Casa de Saúde - ${year}`)
        // Set the year.
        $("#care_house_stats_search").attr('data-year', year)
        // Empty the table.
        $("#care_house_stats_table").html('')
        // Add the year to the download btn.
        $("#care_house_stats_download_btn").attr('data-year', year)
        // Show the modal.
        modal.modal('show')
    }

    /**
     * General function used to get the stats.
     */
    function getStats(searchBtn, careHouse, typology, table, url) {
        // Get the year.
        const year = searchBtn.attr('data-year')
        // Toggle the indicator.
        GenericFunctions.toggleSpinner(searchBtn, true)
        // Prepare the request data.
        const reqData = {
            year: year,
            care_house: careHouse,
            typology: typology
        }
        // Make the ajax request.
        $.ajax({
            url: url,
            type: 'GET',
            data: reqData,
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`,
            },
            success: (data) => {
                const stats = data['data']['stats']
                table.clear()
                table.rows.add(stats).draw(false)
                // const tableId = table.tables().nodes().to$().attr('id')
                GenericFunctions.toggleSpinner(searchBtn, false)
            },
            error: (jq) => {
                GenericFunctions.errorHandler(jq.status, jq.responseText, searchBtn)
            }
        })
    }

    /**
     * Function used to obtain the typology stats data.
     */
    function getTypologyStatsData() {
        if (typologyStatsTable === null) {
            typologyStatsTable = $(`#typology_stats_table`).DataTable({
                columns: [
                    { title: 'Mês' },
                    { title: 'Nº Paciente' },
                    { title: 'Diárias' },
                    { title: 'Diárias (€)' },
                ],
                paging: false,
                ordering: false,
                searching: false,
                info: false
            })
        }

        getStats(
            $("#typology_stats_search"),
            $("#typology_stats_care_house_select").val(),
            $("#typology_stats_typology_select").val(),
            typologyStatsTable,
            "/api/stats/typology/"
        )
    }

    /**
     * Function used to obtain the typology stats data.
     */
    function getCareHouseStatsData() {
        if (careHouseStatsTable === null) {
            careHouseStatsTable = $(`#care_house_stats_table`).DataTable({
                columns: [
                    { title: 'Mês' },
                    { title: 'Nº Paciente' },
                    { title: 'Diárias' },
                    { title: 'Diárias (€)' },
                ],
                paging: false,
                ordering: false,
                searching: false,
                info: false
            })
        }

        getStats(
            $("#care_house_stats_search"),
            $("#care_house_stats_care_house_select").val(),
            $("#care_house_stats_typology_select").val(),
            careHouseStatsTable,
            "/api/stats/care-house/"
        )
    }

    /**
     * Private function used to download XLSX files.
     */
    function downalodXlsxFile(url) {
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
     * Function used to download the typology stats file.
     */
    function downloadTypologyStats(elem) {
        const btn = $(elem)
        // Get the download year.
        const year = btn.attr('data-year')
        // Set the donwload URL.
        const url = "/api/stats/typology/download/?year=" + year

        // Download the file.
        downalodXlsxFile(url)
    }

    /**
     * Function used to download the care house stats file.
     */
    function downloadCareHouseStats(elem) {
        const btn = $(elem)
        // Get the download year.
        const year = btn.attr('data-year')
        // Set the donwload URL.
        const url = "/api/stats/care-house/download/?year=" + year

        // Download the file.
        downalodXlsxFile(url)
    }

    /**
     * Public functions.
     */
    return {
        init: init,
        getTypologyStatsData: getTypologyStatsData,
        getCareHouseStatsData: getCareHouseStatsData,
        showTypologyStatsModal: showTypologyStatsModal,
        showCareHouseStatsModal: showCareHouseStatsModal,
        downloadTypologyStats: downloadTypologyStats,
        downloadCareHouseStats: downloadCareHouseStats
    }
}()

$(document).ready(function () {
    TypologyStats.init()
})