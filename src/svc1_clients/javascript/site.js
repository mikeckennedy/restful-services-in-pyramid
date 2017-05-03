$(document).ready(function () {
    var frm = $('form')

    frm.submit(function (e) {

        loadCarDetails()

        e.preventDefault()
        return false
    })
})

function loadCarDetails() {
    // todo: get car id
    // todo: build url
    // todo: get().done().fail()
}

function populateCarData(car) {
    $("#car_details").fadeOut(function() {

        // todo: set details

        $("#car_details").fadeIn('slow')
    })
}