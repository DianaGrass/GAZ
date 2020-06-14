$("document").ready(function() {
    $('body').on('keyup mouseup', function () {
        $.ajax({"url":"/planning/add_click/"
        })
        console.log("click")
    })
});