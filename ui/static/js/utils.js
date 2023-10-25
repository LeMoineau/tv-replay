function easter_egg() {
    return "hehehe, bien joué grand hacker de la zone ;)"
}

function resetState(expression) {
    $(`${expression}`).each(function() {
        $(this).attr("state", "")
    })
}

function showPanel(idPanel) {
    resetState(".panel")
    $(`#${idPanel}`).attr("state", "show")
}

function fusion(objA, objB) {
    return Object.assign(objA, objB)
}