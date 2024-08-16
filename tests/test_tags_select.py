import pytest
from rapidhtml.tags import Html, Div, Span, P, H1


class TestHtmlSelect:
    def test_select_with_matching_tag_name(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select("div")
        assert len(selected_tags) == 1
        assert isinstance(selected_tags[0], Div)

    def test_select_with_non_matching_tag_name(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select("h1")
        assert len(selected_tags) == 0

    def test_select_with_matching_uninstantiated_subclass(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select(Div)
        assert len(selected_tags) == 1
        assert isinstance(selected_tags[0], Div)

    def test_select_with_non_matching_uninstantiated_subclass(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select(H1)
        assert len(selected_tags) == 0

    def test_select_with_recurse_true(self):
        tag = Html(Div(Span(), P()), Span(), P())
        selected_tags = tag.select("span", recurse=True)
        assert len(selected_tags) == 2
        assert isinstance(selected_tags[0], Span)
        assert isinstance(selected_tags[1], Span)

    def test_select_with_recurse_false(self):
        tag = Html(Div(Span(), P()), Span(), P())
        selected_tags = tag.select("span", recurse=False)
        assert len(selected_tags) == 1
        assert isinstance(selected_tags[0], Span)

    def test_select_with_pop_true(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select("div", pop=True)
        assert len(selected_tags) == 1
        assert isinstance(selected_tags[0], Div)
        assert len(tag.tags) == 2

    def test_select_with_pop_false(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select("div", pop=False)
        assert len(selected_tags) == 1
        assert isinstance(selected_tags[0], Div)
        assert len(tag.tags) == 3

    def test_select_with_first_match_true(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select("div", first_match=True)
        assert len(selected_tags) == 1
        assert isinstance(selected_tags[0], Div)

    def test_select_with_first_match_false(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select("div", first_match=False)
        assert len(selected_tags) == 1
        assert isinstance(selected_tags[0], Div)

    def test_select_with_no_matching_tags_and_pop_true(self):
        tag = Html(Div(), Span(), P())
        with pytest.raises(KeyError):
            tag.select("h1", pop=True)

    def test_select_with_no_matching_tags_and_pop_false(self):
        tag = Html(Div(), Span(), P())
        selected_tags = tag.select("h1", pop=False)
        assert len(selected_tags) == 0

    def test_select_with_instantiated_object(self):
        tag = Html(Div(), Span(), P())
        with pytest.raises(ValueError):
            tag.select(Div())

    def test_select_with_unexpected_tag_type(self):
        tag = Html(Div(), Span(), P())
        with pytest.raises(TypeError):
            tag.select(123)
