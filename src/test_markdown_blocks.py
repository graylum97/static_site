import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )

    def test_markdown_to_blocks_single_paragraph(self):
        md = "This is a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a single paragraph",
            ],
        )

    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# h1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### h6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### not heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##no-space"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        self.assertEqual(
            block_to_block_type("```\ncode line\n```"),
            BlockType.CODE,
        )
        self.assertEqual(
            block_to_block_type("```\ncode line"),
            BlockType.PARAGRAPH,
        )

    def test_quote_blocks(self):
        self.assertEqual(
            block_to_block_type("> quote line"),
            BlockType.QUOTE,
        )
        self.assertEqual(
            block_to_block_type("> first\n> second"),
            BlockType.QUOTE,
        )
        self.assertEqual(
            block_to_block_type("> good\nbad"),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item one"),
            BlockType.ULIST,
        )
        self.assertEqual(
            block_to_block_type("- item one\n- item two"),
            BlockType.ULIST,
        )
        self.assertEqual(
            block_to_block_type("-bad"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first"),
            BlockType.OLIST,
        )
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.OLIST,
        )
        self.assertEqual(
            block_to_block_type("2. not-first"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("1. first\n3. bad-second"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_fallback(self):
        self.assertEqual(
            block_to_block_type("just some text"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("not-a-list\nstill text"),
            BlockType.PARAGRAPH,
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_single_heading(self):
        md = "# My Title\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>My Title</h1></div>")

    def test_multiple_headings_and_paragraphs(self):
        md = """# Title

Some text

## Subtitle

More text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>Some text</p><h2>Subtitle</h2><p>More text</p></div>",
        )

    def test_unordered_list(self):
        md = """- item one
- item two
- item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. first
2. second
3. third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_blockquote(self):
        md = """> quoted
> lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quoted lines</blockquote></div>",
        )

    def test_mixed_blocks(self):
        md = """# Title

- list item with **bold**
- another item

> quote _here_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1>"
            "<ul><li>list item with <b>bold</b></li><li>another item</li></ul>"
            "<blockquote>quote <i>here</i></blockquote>"
            "</div>",
        )

if __name__ == "__main__":
    unittest.main()

