const flashClose = Array.from(document.querySelectorAll(".flash-btn"));

flashClose.forEach(element => {
    element.addEventListener("click", (e)=> {
        element.parentElement.remove()
    })
})
