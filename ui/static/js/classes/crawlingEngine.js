class CrawlingEngine {
    constructor() {
        this.tree = {}
        this.prompt = []
        this.vueController = new VueController()
    }

    crawlChannel(channelName) {
        if (this.tree[channelName] === undefined) {
            this.tree[channelName] = { state: ResourceState.PENDING }
            console.log("channel loading...")
            $.ajax({
                type: "GET",
                url: "/channel",
                data: { name: channelName },
                success: (response) => {
                    this.tree[channelName] = response["channel"]
                    this.prompt = [response["channel"].name]
                    this.vueController.updateMainChannelPanel(`${channelName}-main`, this.tree[channelName])
                }
            });
        }
    }

    crawlNode(node, onsuccess) {
        console.log(node);
        if (node["state"] === undefined) {
            node["state"] = ResourceState.PENDING;
            $.ajax({
                type: "GET",
                url: "/node",
                data: { id: node.id },
                success: function(response) {
                    console.log(response);
                    //update this node in this.tree
                    onsuccess(response)
                }
            });
        }
    }
}