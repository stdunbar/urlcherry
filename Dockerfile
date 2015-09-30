FROM ubuntu

RUN useradd -m -d /home/web web && \
apt-get update && sudo apt-get upgrade -y && \
apt-get install -y libc6 libc6-dev libpython2.7-dev libexpat1-dev libffi-dev python2.7-dev python-pip && \
pip install cherrypy==3.8.0 mako sqlalchemy && \
apt-get autoclean -y && \
apt-get autoremove -y 

USER web
WORKDIR /home/web
ENV PYTHONPATH /home/web

COPY webapp /home/web

USER root
RUN chown -R web.web /home/web

USER web
ENTRYPOINT ["python", "server.py"]
