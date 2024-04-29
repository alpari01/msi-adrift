FROM opendrift/opendrift AS builder

MAINTAINER alpari@taltech.ee

RUN conda config --set solver libmamba

RUN conda install -c conda-forge uwsgi

COPY requirements.txt requirements.txt

RUN pip3 install Cython
RUN pip3 install -r requirements.txt
RUN pip3 install pytest pytest-cov mock coverage

RUN useradd -ms /bin/bash uwsgi

RUN mkdir /output && mkdir /input

COPY webapp /webapp
RUN chown -R uwsgi:uwsgi /output /input /webapp

COPY __init__.py /code/opendrift/models/basemodel/

USER uwsgi
WORKDIR /webapp
EXPOSE 8080
CMD ["uwsgi", "--enable-threads", "--http", ":8080", "--wsgi-file", "wsgi.py"]
