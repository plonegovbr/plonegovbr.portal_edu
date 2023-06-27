# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6
FROM plone/server-builder:${PLONE_VERSION} as builder

WORKDIR /app

# Add local code
COPY sources sources
COPY . src/plonegovbr.portal_edu

# Install local requirements and pre-compile mo files
RUN <<EOT
    set -e
    mv src/plonegovbr.portal_edu/requirements-docker.txt ./requirements.txt
    bin/pip install -r requirements.txt
    bin/python /compile_mo.py
    rm -Rf src/ sources/ /compile_mo.py compile_mo.log
EOT

FROM plone/server-prod-config:${PLONE_VERSION}

LABEL maintainer="PloneGov-Br <portalbrasil@plone.org.br>" \
      org.label-schema.name="ghcr.io/plonegovbr/portal_edu" \
      org.label-schema.description="Uma distribuição Plone para instituições de ensino brasileiras." \
      org.label-schema.vendor="PloneGov-Br"

# Disable MO Compilation
ENV zope_i18n_compile_mo_files=
# Show only our distributions
ENV ALLOWED_DISTRIBUTIONS=portal_edu

COPY --from=builder /app /app

RUN <<EOT
    ln -s /data /app/var
EOT
