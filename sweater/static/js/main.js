document.querySelectorAll(".card-info").forEach((element) => {
    if (element.childElementCount === 2) {
        element.classList.add('card-info-pointer')
        let el1 = element.children[0]
        let el2 = element.children[1]

        element.addEventListener("click", () => {
            if (el2.classList.contains('hidden')) {
                el1.classList.add('fade-out')
            } else {
                el2.classList.add('fade-out')
            }
            setTimeout(() => {
                el1.classList.remove('fade-out')
                el2.classList.remove('fade-out')

                el1.classList.toggle('hidden')
                el2.classList.toggle('hidden')

                el1.classList.toggle('fade-in')
                el2.classList.toggle('fade-in')

            }, 500)
        })
    }
})