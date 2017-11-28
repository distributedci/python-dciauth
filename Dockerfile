FROM centos:7

LABEL name="DCI AUTH"
MAINTAINER DCI Team <distributed-ci@redhat.com>

RUN yum -y install epel-release && \
    yum -y install python python-devel python-tox python2-pip && \
    yum clean all

RUN mkdir /opt/python-dciauth
WORKDIR /opt/python-dciauth
COPY requirements.txt /opt/python-dciauth/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /opt/python-dciauth/

ENV PYTHONPATH /opt/python-dciauth

CMD ["tail", "-f", "/dev/null"]
