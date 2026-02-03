class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        parts = []
        for key, value in self.props.items():
            part = f' {key}="{value}"'
            parts.append(part)
        return "".join(parts)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(
            tag=tag,
            value=value,
            children=None,
            props=props,
        )

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        props_str = self.props_to_html()

        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(
            tag=tag,
            children=children,
            props=props,
        )

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        props_str = self.props_to_html()

        open_tag = f"<{self.tag}{props_str}>"
        close_tag = f"</{self.tag}>"

        return open_tag + children_html + close_tag
