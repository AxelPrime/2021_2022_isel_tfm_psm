'use strict'

let Notifications = function () {
    /**
     * Initialization function.
     */
    function init() {

    }

    /**
     * Function used to redirect a click on a notification.
     */
    function redirectNotification(elem) {
        const btn = $(elem)

        // Obtain the notification data.
        const id = btn.attr('data-notification-id')
        const readable = btn.attr('data-readable') === 'True'
        const link = btn.attr('data-link')

        // Check if the notification is readable.
        if (readable) {
            // Mark the notification as read.
            $.ajax({
                url: "/api/users/notifications/read/",
                type: "POST",
                data: JSON.stringify({
                    notification_id: id
                }),
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `Token ${Cookies.get('userToken')}`,
                },
                success: function (data) {
                    window.location.href = link
                },
                error: function (jq) {
                    GenericFunctions.errorHandler(jq.status, jq.responseText)
                }
            })
        } else window.location.href = link
    }

    /**
     * Function used to obtain the current user's notifications.
     */
    function getNotifications() {
        $.ajax({
            url: "/api/users/notifications/",
            type: 'GET',
            headers: {
                'Authorization': `Token ${Cookies.get('userToken')}`,
            },
            success: (data) => {
                const notifications = data['data']['notifications']
                const count = data['data']['count']

                buildNotificationsMenu(notifications, count)
            },
            error: (jq) => {
                GenericFunctions.errorHandler(jq.status, jq.responseText)
            }
        })
    }

    /**
     * Function used to build the notifications' menu.
     */
    function buildNotificationsMenu(notifications, count) {
        const menuCount = (count) ?
            `<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger fs-6">
                ${count}
            </span>` : ``

        let notificationsHtml = ``
        for (let i = 0; i < notifications.length; i++) {
            let n = notifications[i]
            notificationsHtml += `
                <div class="d-flex flex-row mx-3 align-items-center bg-hover-primary py-2" data-notification-id="${ n.id }" data-readable="${ n.readable }" data-link="${ n.link }" onclick="Notifications.redirectNotification(this)" style="cursor: pointer; ">
                    <div class="d-flex flex-column align-items-center">
                        <div class="{{ n.bg }} p-2 fs-5 text-white rounded-circle">
                            <div class="d-flex justify-content-center align-items-center" style="height: 30px; width: 30px">
                                <div class="pt-2">
                                    <i class="${ n.icon } fs-3"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex flex-column align-items-center">
                        <div class="ms-2">
                            <div class="d-flex flex-row align-items-center">
                                <div class="d-flex flex-column fw-bolder fs-5">
                                    ${ n.title }
                                </div>
                                <div class="d-flex flex-column ms-2 fs-6">
                                    ${ n.date }
                                </div>
                            </div>
                            <div class="d-flex flex-row justify-content-start">
                                ${ n.text }
                            </div>
                        </div>
                    </div>
                </div>
            `
        }

        const html = `
            <i class="bi bi-bell fs-4 me-2" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">
                ${menuCount}
            </i>
            <div class="dropdown-menu shadow shadow-sm" style="width: 350px">
                ${(count) ? notificationsHtml : `<div class="m-3 fs-5 fw-bolder justify-content-center d-flex">Não tem notificações</div>`}
            </div>
        `
        $("#notifications_dropdown").html(html)
    }

    return {
        init: init,
        redirectNotification: redirectNotification,
        getNotifications: getNotifications,
    }
}()

$(document).ready(function () {
    Notifications.init()
})