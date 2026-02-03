FROM golang:1-trixie AS makehtml

# Add Hugo build options, e.g. --buildDrafts --buildFuture
ARG HUGO_BUILDOPTS

RUN apt update
# RUN apt install -y golang
# RUN apt install -y ssh

# Configuration variables
# ENV GIT_REPO_CONTENT_PATH=''
# ENV GIT_REPO_BRANCH='main'
# ENV TARGET_DIR='/target'
# ENV GIT_SSH_ID_FILE='/ssh/id_rsa'

# Install go packages
RUN go install github.com/go-task/task/v3/cmd/task@latest
# RUN go install github.com/mikefarah/yq/v4@latest
RUN go install github.com/gohugoio/hugo@latest
RUN echo 'export PATH=$PATH:/root/go/bin' >>  /root/.bashrc

WORKDIR /build

COPY archetypes /build/archetypes
COPY assets /tmp/assets
COPY content /build/content
COPY data /build/data
COPY i18n /build/i18n
COPY layouts /build/layouts
COPY static /build/static
COPY themes /build/themes

COPY hugo.yaml /build/hugo.yaml
COPY go.mod /build/go.mod
COPY go.sum /build/go.sum
COPY Taskfile.yaml /build/Taskfile.yaml

ARG HUGO_BASEURL=https://opendata.lib.umd.edu/
ENV HUGO_BASEURL=$HUGO_BASEURL

RUN hugo build --minify --destination /build/html ${HUGO_BUILDOPTS}

FROM nginx:1.20
COPY --from=makehtml /build/html /usr/share/nginx/html
