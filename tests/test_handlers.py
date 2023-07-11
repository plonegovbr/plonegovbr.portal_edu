from pathlib import Path
from plone import api
from plone.distribution.api import distribution as dist_api
from plonegovbr.portal_edu import handlers

import logging.config


DISTRIBUTION_NAME = "portal_edu"


class TestHandlers:
    def test_post_handler_logo(self, portal):
        logging.config.fileConfig(
            Path("instance/etc/zope.ini"), disable_existing_loggers=False
        )
        raw_logo = "name=teste;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        expected_result = b"filenameb64:dGVzdGU7ZGF0YTppbWFnZS9wbmc=;datab64:iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        distribution = dist_api.get(name=DISTRIBUTION_NAME)
        handlers.post_handler(distribution, portal, answers={"logo": raw_logo})
        with open(Path("instance/var/log/instance.log")) as f:
            last_line = f.readlines()[-1]
        assert api.portal.get_registry_record("plone.site_logo") == expected_result
        assert "Logo atualizado" in last_line
