FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip && apt-get upgrade -y && apt-get autoremove -y
RUN mkdir -p /user/k8soper && mkdir -p /app && mkdir -p /app/templates/ && mkdir -p /app/static/
ADD . /app
ADD ./templates/index.html /app/templates/index.html
ADD ./static/* /app/static/

RUN pip3 install -r /app/requirements.txt
RUN ln -s /usr/bin/python3.8 /usr/local/bin/python

RUN useradd k8soper --uid 9999 -M -U --home-dir /user/k8soper
USER k8soper
WORKDIR /user/k8soper
EXPOSE 5000
CMD ["python", "/app/app.py"]