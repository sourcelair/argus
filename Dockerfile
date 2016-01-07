FROM python:2.7
MAINTAINER Thanasis Daglis <ath.daglis@gmail.com>

EXPOSE 5000

# Install argus
ADD argus /opt/argus
WORKDIR /opt/argus
RUN python setup.py install
RUN rm -r /opt/argus
