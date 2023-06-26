import pytest


class TestControlPanelPBEdu:
    CONFIGLET_ID: str = "pb_edu"

    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal
        self.control_panels = portal["portal_controlpanel"]
        filtered = [
            configlet
            for configlet in self.control_panels.listActions()
            if configlet.id == self.CONFIGLET_ID
        ]
        self.control_panel = filtered[0] if filtered else None

    def test_pb_edu_exists(self):
        assert self.control_panel

    def test_pb_edu_is_visible(self):
        assert self.control_panel.visible

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ["appId", "pb_edu-controlpanel"],
            ["id", "pb_edu"],
            ["title", "PortalBrasil.edu: Configurações"],
        ],
    )
    def test_controlpanel_attributes(self, attr, expected):
        assert getattr(self.control_panel, attr, None) == expected
