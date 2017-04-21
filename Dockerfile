FROM        ubuntu:16.04

RUN         apt-get -y update
RUN         apt-get -y install git

WORKDIR     srv/
RUN         git clone https://github.com/CressZZ/gori_bundle.git front
COPY        .  app