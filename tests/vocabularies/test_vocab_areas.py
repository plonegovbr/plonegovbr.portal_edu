from plone import api
from plonegovbr.portal_base import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabAvailableAreas:
    name = f"{PACKAGE_NAME}.vocab.available_areas"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        ["sociais", "engenharia", "tecnologia"],
    )
    def test_token(self, token):
        assert token in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token,title",
        [
            ["sociais", "Ciências Sociais"],
            ["engenharia", "Engenharias"],
            ["tecnologia", "Tecnologia"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title


class TestVocabAreas:
    name = f"{PACKAGE_NAME}.vocab.areas"

    @pytest.fixture(autouse=True)
    def _init(self, get_vocabulary, portal, cursos):
        self.portal = portal
        for curso_uid in cursos:
            obj = api.content.find(UID=curso_uid)[0].getObject()
            obj.reindexObject()
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token",
        [
            "sociais",
            "tecnologia",
        ],
    )
    def test_token(self, token):
        assert token in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token",
        [
            "engenharia",
        ],
    )
    def test_token_not_in(self, token):
        assert token not in [x for x in self.vocab.by_token]

    @pytest.mark.parametrize(
        "token,title",
        [
            ["sociais", "Ciências Sociais"],
            ["tecnologia", "Tecnologia"],
        ],
    )
    def test_token_title(self, token, title):
        term = self.vocab.getTerm(token)
        assert title == term.title

    def test_qs(self):
        """Test qs."""
        querybuilder = api.content.get_view("querybuilderresults", context=self.portal)
        query = [
            {
                "i": "areas",
                "o": "plone.app.querystring.operation.selection.any",
                "v": ["sociais"],
            }
        ]
        results = querybuilder(query=query)
        assert len(results) == 1
