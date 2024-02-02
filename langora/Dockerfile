FROM python:3.9.18-bullseye

RUN pip3 install --upgrade pip setuptools

#pytorch
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

#Application Install
WORKDIR /app
ADD requirements.txt .
RUN pip3 install -r requirements.txt

#playwright (chromium install)
RUN playwright install
RUN playwright install-deps

#supervisor
RUN apt-get update && apt-get install -y supervisor
ADD app/task/supervisord.conf /etc/supervisor/

ENV IN_DOCKER Yes