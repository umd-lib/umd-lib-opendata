
FROM debian:stable-slim

RUN apt update && apt install -y curl webhook git golang python3 rclone

# Configuration variables
ENV GIT_REPO_CONTENT_PATH=''
ENV GIT_REPO_BRANCH='main'

# Pinned so upstream releases can't break this build; bump deliberately after
# verifying "task build" locally with the new version.
ARG TASK_VERSION=v3.52.0
ARG HUGO_VERSION=v0.164.0

# Install go packages
RUN go install github.com/go-task/task/v3/cmd/task@${TASK_VERSION}
RUN go install github.com/gohugoio/hugo@${HUGO_VERSION}
RUN echo 'export PATH=$PATH:/root/go/bin' >>  /root/.bashrc

WORKDIR /tmp

# Expose default webhook port
EXPOSE 9000

COPY hooks.json /etc/hooks.json
COPY rclone.conf /etc/rclone.conf

COPY scripts /scripts

CMD [ "/usr/bin/webhook", "-hooks", "/etc/hooks.json", "-template", "-verbose", "-logfile", "/dev/fd/1" ]