
FROM debian:stable-slim

RUN apt update && apt install -y curl webhook git golang python3

# Configuration variables
ENV GIT_REPO_CONTENT_PATH=''
ENV GIT_REPO_BRANCH='main'
ENV TARGET_DIR='/target'

# Install go packages
RUN go install github.com/go-task/task/v3/cmd/task@latest
RUN go install github.com/gohugoio/hugo@latest
RUN echo 'export PATH=$PATH:/root/go/bin' >>  /root/.bashrc

WORKDIR /tmp

# Expose default webhook port
EXPOSE 9000

COPY hooks.json /etc/hooks.json

COPY scripts /scripts

CMD [ "/usr/bin/webhook", "-hooks", "/etc/hooks.json", "-template", "-verbose", "-logfile", "/dev/fd/1" ]