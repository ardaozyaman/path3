FROM jenkins/jenkins:lts
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wget gnupg2 ca-certificates unzip fonts-liberation libu2f-udev libasound2 libnss3 libxss1 lsb-release
RUN apt-get update && \
    apt-get install -y chromium chromium-driver libgbm1 libdrm2 libxshmfence1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN jenkins-plugin-cli --plugins workflow-aggregator git github htmlpublisher
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libasound2 \
    libgbm1 \
    libdrm2 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*
USER jenkins