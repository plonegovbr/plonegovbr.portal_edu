from plone import api
from plone.distribution.core import Distribution
from plonegovbr.portal_base.utils.handlers import ajusta_idioma
from plonegovbr.portal_base.utils.handlers import converte_logo_data
from plonegovbr.portal_edu import logger
from Products.CMFPlone.Portal import PloneSite


def post_handler(
    distribution: Distribution, site: PloneSite, answers: dict
) -> PloneSite:
    """Processa o site criado e realiza pequenos ajustes."""
    name = distribution.name
    # Ajusta o idioma para pt-br
    ajusta_idioma(site)
    raw_logo = answers.get("logo")
    if raw_logo:
        logo = converte_logo_data(raw_logo)
        api.portal.set_registry_record("plone.site_logo", logo)
        logger.info(f"{name}: Logo atualizado")
    return site
