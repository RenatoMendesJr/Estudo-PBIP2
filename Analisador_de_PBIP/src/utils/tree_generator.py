def generate_tree_diagram(json_data, output_dot_file):
    from anytree import Node
    from anytree.exporter import DotExporter

    def create_tree(data, parent_node):
        if isinstance(data, dict):
            for key, value in data.items():
                child_node = Node(key, parent=parent_node)
                create_tree(value, child_node)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                child_node = Node(f"Item {index}", parent=parent_node)
                create_tree(item, child_node)
        else:
            Node(str(data), parent=parent_node)

    root = Node("root")
    create_tree(json_data, root)
    DotExporter(root).to_dotfile(output_dot_file)