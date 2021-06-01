document.querySelectorAll(".nav-link").forEach((element) => {
    element.addEventListener("click", () => {
        document.body.classList.add('fade-out')
        setTimeout(() => {document.body.classList.add('non-visible')}, 800)
    })
})

$(document).ready(() => {
    document.body.classList.add('fade-in')
    document.body.classList.remove('non-visible')
})


$('.toast').toast(autohide=true)
$('#liveToast').toast('show')