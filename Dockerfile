FROM ubuntu

RUN useradd -m -d /home/web web && mkdir /home/web/.venv &&\

apt-get update && sudo apt-get upgrade -y && \
apt-get install -y libc6 libc6-dev libpython2.7-dev libpq-dev libexpat1-dev libffi-dev libssl-dev python2.7-dev python-pip postgresql && \
pip install virtualenv && \
pip install cython && \
pip install cherrypy==3.6.0 pyopenssl mako psycopg2 python-memcached sqlalchemy && \
apt-get autoclean -y && \
apt-get autoremove -y 

USER web
WORKDIR /home/web
ENV PYTHONPATH /home/web/webapp

COPY webapp /home/web/webapp

ENTRYPOINT ["cherryd", "-i", "server"]
