import pytest

import rapidhtml.exceptions
from rapidhtml.tags import Div


class TestCyclicalTag:
    def test_cyclical_tag(self):
        tag = Div()
        with pytest.raises(rapidhtml.exceptions.CyclicalTagError):
            tag.add_tag(tag)

    def test_cyclical_tag_with_multiple_tags(self):
        tag1 = Div()
        tag2 = Div()
        with pytest.raises(rapidhtml.exceptions.CyclicalTagError):
            tag1.add_tag(tag2)
            tag2.add_tag(tag1)

    def test_cyclical_tag_with_multiple_tags_and_no_cyclical_error(self):
        tag1 = Div()
        tag2 = Div()
        tag1.add_tag(tag2)
        assert True
