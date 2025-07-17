FROM sphinxdoc/sphinx:4.5.0 AS makehtml

WORKDIR /docs
COPY source source
COPY Makefile .
RUN pip install sphinx-sitemap==2.6.0
RUN make html

FROM nginx:1.20
COPY --from=makehtml /docs/build/html /usr/share/nginx/html
