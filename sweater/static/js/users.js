$(document).ready(() => {
    $("#usersTable").DataTable({
        "responsive": true,
        "fixedHeader": true,
        "lengthChange": false,
        "pageLength": 10,
        "language": {
            "zeroRecords": "Не найдено",
            "info": "Страница _PAGE_ из _PAGES_",
            "infoEmpty": "Нет доступных анкет",
            "infoFiltered": "(Отфильтровано из всех _MAX_ анкет)",
            "search": "Поиск ",
            "paginate": {
                "first": "Первая",
                "last": "Последняя",
                "next": "Вперёд",
                "previous": "Назад"
            }
        }
    })
})
