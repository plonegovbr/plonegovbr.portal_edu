from base64 import b64encode
from plone import api
from plone.distribution.core import Distribution
from plonegovbr.portal_edu import logger
from Products.CMFPlone.Portal import PloneSite


def ajusta_idioma(site: PloneSite, language: str = "pt-br"):
    """Seta o idioma do site para pt-br."""
    # Ajusta conteúdo
    site.setLanguage(language)


def converte_logo_data(logo: str):
    """Converte os dados do logo de data-uri para o formato to registro do Plone."""
    headers, data = logo.split("base64,")
    filename = headers.split("name=")[1][:-1]
    filenameb64 = b64encode(filename.encode("utf-8")).decode("utf-8")
    response = f"filenameb64:{filenameb64};datab64:{data}"
    return response.encode("utf-8")


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
