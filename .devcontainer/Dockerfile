FROM python:3.12.8-bookworm

RUN apt-get update && \
    apt install curl apt-transport-https gnupg2 software-properties-common -y && \
    apt update && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt install nodejs -y && \
    npm install -g npm@11.0.0

ARG USERNAME=taktile
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

ENV SHELL /bin/bash
ENV PATH /home/$USERNAME/.local/bin:$PATH




