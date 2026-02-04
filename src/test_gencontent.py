from gencontent import extract_title

def test_extract_title_basic():
    md = "# Hello"
    assert extract_title(md) == "Hello"

def test_extract_title_spaces():
    md = "#  Hello there  "
    assert extract_title(md) == "Hello there"

def test_extract_title_no_h1_raises():
    md = "## Not an h1"
    raised = False
    try:
        extract_title(md)
    except Exception:
        raised = True

    assert raised
