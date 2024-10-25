import random

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

    def test_deep_cyclical_tag(self):
        NUM_TAGS = 1_000

        root_tag = Div()
        tag_list = [Div() for _ in range(NUM_TAGS)]

        # Add all tags to the root tag
        root_tag.add_tag(*tag_list)

        # Add all tags that come AFTER the current iteration of tag
        sample_tag_index = random.randint(0, NUM_TAGS - 1)
        tag_list[sample_tag_index].add_tag(*tag_list[sample_tag_index + 1 :])

        with pytest.raises(rapidhtml.exceptions.CyclicalTagError):
            tag_list[-1].add_tag(root_tag)
