class VueController {
    constructor() {
        this.prompt = []
    }

    updateMainChannelPanel(panelID, node) {
        let panel = $(`#${panelID}`);
        this.prompt = [node.title]
        this.displayNode(node, panel)
    }

    displayNode(node, panel) {
        console.log("displaying node", node)
        panel.html('')
        let supheader = $(`<div class="panel-sup-header"> <p>${this.prompt.join('/') + '/'}</p> <a href="${node.url}"> at <u>${node.url}</u> </a> </div>`)
        let title = $(`<div class="panel-title"> </div>`)
        title.append(`<h1> ${node.title} </h1>`)
        let description = $(`<p class="panel-description"></p>`)
        if (node.type === "Categorie") {
            title.append(`<span class="tag tag-categorie"> Catégorie </span>`)
            description.append("Cette catégorie contient les éléments suivants: ")
        } else if (node.type === "Section") {
            title.append(`<span class="tag tag-section"> Section </span>`)
            description.append("Cette section contient les éléments suivants: ")
        } else if (node.type === "Video") {
            title.append(`<span class="tag tag-video"> Vidéo </span>`)
            description.append("Cette vidéo contient les éléments suivants: ")
        } else { // is channel
            title.append(`<span class="tag tag-site"> Site </span>`)
            description.append("Cette catégorie contient les catégories suivants: ")
        }
        panel.append(supheader)
        panel.append(title)
        panel.append(description)
        for (let id in node.children) {
            this.displayNodeLine(node.children[id], panel)
        }
    }

    displayNodeLine(nodeChild, panel) {
        let line = $(`<div class="panel-flexline"> </div>`)
        line.click(() => {
            crEngine.crawlNode(nodeChild, (node) => {
                this.prompt.push(node.title)
                this.displayNode(node, panel)
            })
        })
        let left = $(`<div class="panel-flexline-left"></div>`)
        if (nodeChild.type === "Categorie") {
            left.append(`<span class="tag tag-categorie"> Catégorie </span>`)
        } else if (nodeChild.type === "Section") {
            left.append(`<span class="tag tag-section"> Section </span>`)
        } else if (nodeChild.type === "Video") {
            left.append(`<span class="tag tag-video"> Vidéo </span>`)
        } else { // is channel
            left.append(`<span class="tag tag-site"> Site </span>`)
        }
        left.append(`<h2> ${nodeChild.title} </h2>`)
        line.append(left)
        line.append(`<div class="panel-flexline-right"> <a href="${nodeChild.url}"> at <u> ${nodeChild.url} </u> </a> </div>`)
        panel.append(line)
    }

    displayTable(dico, header = ["title", "url"]) {
        let table = $(`<table class="panel-table"></table>`);
        let line = $(`<tr></tr>`);
        for (let h of header) {
            line.append(`<th> ${h} </th>`);
        }
        table.append(line);
        for (let id in dico) {
            line = $(`<tr class="panel-table-line"></tr>`);
            line.click(() => {
                crEngine.crawlNode(dico[id], (node) => {
                    this.prompt.push(response.title)
                    this.displayNode(node, )
                })
            })
            for (let k in dico[id]) {
                if (header.includes(k))
                    line.append(`<td> ${dico[id][k]} </td>`);
            }
            table.append(line);
        }
        return table;
    }
}