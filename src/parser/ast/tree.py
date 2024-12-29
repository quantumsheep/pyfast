from dataclasses import fields, is_dataclass

from treelib import Tree

from parser.ast.base import SourceFile, SourcePosition


def to_tree(instance: object) -> Tree:
    tree = Tree()

    def format_value(value: object) -> str:
        if isinstance(value, str):
            return f'"{value}"'.translate(str.maketrans({'"': r"\""}))
        return str(value)

    def _to_tree(instance: object, parent_id: str) -> None:
        if not is_dataclass(instance):
            return

        for field in fields(instance):
            value = getattr(instance, field.name)
            if isinstance(value, SourcePosition):
                continue
            if isinstance(instance, SourceFile) and field.name == "content":
                continue

            field_node_id = f"{parent_id}.{field.name}"
            field_node_tag = f"{field.name}"

            if is_dataclass(value):
                tree.create_node(
                    f"{field_node_tag}: {type(value).__name__}",
                    field_node_id,
                    parent=parent_id,
                )
                _to_tree(value, field_node_id)
            elif isinstance(value, list):
                tree.create_node(field_node_tag, field_node_id, parent=parent_id)

                for i, item in enumerate(value):
                    item_node_id = f"{field_node_id}[{i}]"
                    item_node_tag = f"{i}"

                    if not is_dataclass(item):
                        item_node_tag += f": {format_value(item)}"
                    else:
                        item_node_tag += f": {type(item).__name__}"

                    tree.create_node(item_node_tag, item_node_id, parent=field_node_id)

                    _to_tree(item, item_node_id)
            else:
                tree.create_node(
                    f"{field_node_tag}: {format_value(value)}",
                    field_node_id,
                    parent=parent_id,
                )

    tree.create_node("program", "program")
    _to_tree(instance, "program")

    return tree
