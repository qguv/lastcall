FROM frolvlad/alpine-python3
MAINTAINER Quint Guvernator <quint@guvernator.net>

# grab dependencies
RUN pip3 install --upgrade pip
RUN pip3 install certifi
RUN pip3 install googlemaps

# add the project
RUN mkdir -p /srv/lastcall
WORKDIR /srv/lastcall
ADD src .

# run the project
CMD ["python3", "lastcall.py"]
