from plone import api
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component.hooks import setSite

import pytest


@pytest.fixture()
def portal(portal_edu):
    setSite(portal_edu)
    return portal_edu


class TestDistributionPortalEdu:
    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Universidade Livre"),
            ("description", "Site da Universidade Livre do Brasil"),
            ("exclude_from_nav", False),
        ],
    )
    def test_plone_site_attributes(self, attr, expected):
        assert getattr(self.portal, attr) == expected

    @pytest.mark.parametrize(
        "package,expected",
        [
            ("plone.app.contenttypes", True),
            ("plone.app.caching", True),
            ("plonetheme.barceloneta", True),
            ("plone.restapi", True),
            ("plone.volto", True),
            ("plonegovbr.portal_base", True),
            ("collective.contact_behaviors", True),
            ("collective.person", True),
        ],
    )
    def test_dependencies_installed(self, installer, package, expected):
        assert installer.is_product_installed(package) is expected

    @pytest.mark.parametrize(
        "path,title,portal_type,review_state",
        [
            ("/", "Universidade Livre", "Plone Site", ""),
        ],
    )
    def test_content_created(self, path, title, portal_type, review_state):
        with api.env.adopt_roles(
            [
                "Manager",
            ]
        ):
            content = api.content.get(path=path)
        assert content.title == title
        assert content.portal_type == portal_type
        if review_state:
            assert api.content.get_state(content) == review_state
        else:
            with pytest.raises(WorkflowException) as exc:
                api.content.get_state(content)
            assert "No workflow provides" in str(exc)

    @pytest.mark.parametrize(
        "portal_type,global_allow",
        [
            ("Campus", True),
            ("Curso", True),
            ("Person", True),
        ],
    )
    def test_types_available(self, get_fti, portal_type, global_allow):
        fti = get_fti(portal_type)
        assert fti.global_allow is global_allow

    @pytest.mark.parametrize(
        "portal_type,allowed",
        [
            ("Campus", True),
            ("Curso", True),
            ("Person", False),
        ],
    )
    def test_types_in_navigation(self, portal_type, allowed):
        types = api.portal.get_registry_record("plone.displayed_types")
        is_in_navigation = portal_type in types
        assert is_in_navigation is allowed
