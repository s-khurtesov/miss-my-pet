#!/bin/bash

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
sudo apt-get install apt-transport-https ca-certificates gnupg && \
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
sudo apt-get update && sudo apt-get install google-cloud-sdk && \
gcloud init && \
gcloud auth application-default login && \
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy && \
chmod +x cloud_sql_proxy

exit $?
