def node_to_json(node):
    """
    Transforme une classe [Node] (Video, Section, Channel..etc) en json

    parameters:
    - node: [Node] a transformer en json

    returns:
    - res: json decrivant [node]
    """
    res = vars(node).copy()

    # gestion cas particuliers
    children = {}
    for c in res["children"]:
        children[c.id] = node_to_json(c)
    res["children"] = children

    if "crawler" in res:
        del res["crawler"]
    if res["parent"] is not None:
        res["parent"] = res["parent"].id
    if "downloader" in res:
        del res["downloader"]
    if "html_element" in res:
        del res["html_element"]

    res["type"] = node.get_type_str()

    # retour de la finalité, leeeet's go
    return res
