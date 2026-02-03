import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr_runs(self):
        node = HTMLNode("p", "hello")
        repr(node)  # just ensure it doesn't crash


    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click", {"href": "https://example.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click</a>',
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag_returns_raw_text(self):
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    def test_leaf_to_html_raises_when_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag_raises(self):
        child = LeafNode("span", "child")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_multiple_children(self):
        c1 = LeafNode(None, "first")
        c2 = LeafNode("i", "second")
        c3 = LeafNode(None, "third")
        node = ParentNode("p", [c1, c2, c3])
        self.assertEqual(
            node.to_html(),
            "<p>first<i>second</i>third</p>",
        )

    def test_to_html_deep_nesting(self):
        inner = LeafNode("b", "inner")
        mid = ParentNode("span", [inner])
        outer = ParentNode("div", [mid])
        self.assertEqual(
            outer.to_html(),
            "<div><span><b>inner</b></span></div>",
        )

    def test_to_html_siblings_parents(self):
        c1 = ParentNode("span", [LeafNode(None, "one")])
        c2 = ParentNode("span", [LeafNode(None, "two")])
        parent = ParentNode("div", [c1, c2])
        self.assertEqual(
            parent.to_html(),
            "<div><span>one</span><span>two</span></div>",
        )

    def test_to_html_child_leaf_no_tag(self):
        text_child = LeafNode(None, "hello")
        node = ParentNode("p", [text_child])
        self.assertEqual(node.to_html(), "<p>hello</p>")

    def test_parent_to_html_with_props(self):
        child = LeafNode(None, "text")
        node = ParentNode("p", [child], {"class": "cls"})
        self.assertIn('<p class="cls">text</p>', node.to_html())

if __name__ == "__main__":
    unittest.main()
