
$('#Modal').on('show.bs.modal', function (event) {
    const modal = $(this)
    const user = $(event.relatedTarget).data('name')
    const question = $(event.relatedTarget).data('question')
    const date = $(event.relatedTarget).data('date')
    const uid = $(event.relatedTarget).data('uid')
    const qid = $(event.relatedTarget).data('qid')

    modal.find('.modal-title').text('Вопрос пользователя ' + user)
    modal.find('.card-date').text("Время: " + date)
    modal.find('#q-text')[0].value = question
    modal.find('#uid')[0].value = uid
    modal.find('#qid')[0].value = qid
    modal.find('#text')[0].value = ''
})