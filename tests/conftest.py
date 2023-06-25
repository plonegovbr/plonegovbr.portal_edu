from plone import api
from plonegovbr.portal_edu.testing import FUNCTIONAL_TESTING
from plonegovbr.portal_edu.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (FUNCTIONAL_TESTING, "functional"),
            (INTEGRATION_TESTING, "integration"),
        )
    )
)


@pytest.fixture
def campi_payload() -> list:
    """Payload to create two campus items."""
    return [
        {
            "type": "Campus",
            "id": "curitiba",
            "title": "Campus Curitiba",
            "description": "Campus Curitiba da UTFPR",
            "contact_email": "curitiba@utfpr.edu.br",
            "contact_website": "https://portal.utfpr.edu.br/campus/curitiba",
            "contact_phone": "+55 (41) 3310-4545",
            "address": "Av. Sete de Setembro, 3165",
            "address_2": "Rebouças",
            "city": "Curitiba",
            "state": "PR",
            "postal_code": "80230-901",
            "country": "BR",
        },
        {
            "type": "Campus",
            "id": "campos-centro",
            "title": "Campos Centro",
            "description": "IFFluminense Campus Campos Centro",
            "contact_email": "gabinete.camposcentro@iff.edu.br",
            "contact_website": "https://iff.edu.br/nossos-campi/campos-centro",
            "contact_phone": "+55 (22) 2726-2800",
            "address": "Rua Dr. Siqueira, 273 ",
            "address_2": "Parque Dom Bosco",
            "city": "Campos dos Goytacazes",
            "state": "RJ",
            "postal_code": "28030-130",
            "country": "BR",
        },
    ]


@pytest.fixture
def campi(portal, campi_payload) -> dict:
    """Create Campus content items."""
    response = {}
    with api.env.adopt_roles(
        [
            "Manager",
        ]
    ):
        for data in campi_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture
def campus(campi) -> dict:
    """Return one Campus."""
    content_uid = [key for key in campi.keys()][0]
    brains = api.content.find(UID=content_uid)
    return brains[0].getObject()


@pytest.fixture
def cursos_payload() -> list:
    """Payload to create two curso items."""
    return [
        {
            "type": "Curso",
            "id": "pgp-curitiba",
            "title": "PGP- Curitiba",
            "description": "Pós-Graduação em Planejamento e Governança Pública",
            "modalidades": ["mestrado"],
            "areas": ["sociais"],
        },
        {
            "type": "Curso",
            "id": "tecnico-integrado-em-informatica",
            "title": "Curso Técnico Integrado em Informática",
            "description": "A informática está inserida em todos os segmentos...",
            "modalidades": ["tecnico"],
            "areas": ["tecnologia"],
        },
    ]


@pytest.fixture
def cursos(portal, cursos_payload) -> dict:
    """Create Curso content items."""
    response = {}
    with api.env.adopt_roles(
        [
            "Manager",
        ]
    ):
        for data in cursos_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture
def curso(cursos) -> dict:
    """Return one Curso."""
    content_uid = [key for key in cursos.keys()][0]
    brains = api.content.find(UID=content_uid)
    return brains[0].getObject()
