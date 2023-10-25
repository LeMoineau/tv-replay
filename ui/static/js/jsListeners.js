// Header listener
$("#nav-header").click(function() {
    showPanel("main-panel")
    resetState(".nav-button[state='selected']")
})

// Nav buttons listeners
$(".nav-button-content").click(function() {
    let parent = $(this).parent()
    if (parent.attr("state") === "selected") {
        parent.attr("state", "")
    } else {
        resetState(".nav-button[state='selected']")
        parent.attr("state", "selected")
        let linkSelected = parent.children("div.nav-button-sublevel").children("a.nav-button-sublevel-link[state='selected']")
        if (linkSelected.length > 0) {
            _selectNavButtonLink(linkSelected)
        }
    }
})

// Nav buttons sections selecter
$("a.nav-button-sublevel-link").click(function() {
    resetState("a.nav-button-sublevel-link[state='selected']")
    $(this).attr("state", "selected")
    _selectNavButtonLink($(this))
})

/**
 * Execute toutes les fonctions necessaires lors de la selection d'un lien d'un bouton de navigation
 * @param {JQueryElement} ele element HTML du lien
 */
function _selectNavButtonLink(ele) {
    showPanel(ele.attr("panel"))
    eval(ele.attr("func"))
}