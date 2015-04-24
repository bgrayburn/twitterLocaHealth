FROM opentable/anaconda

COPY . /root/src/
EXPOSE 80

CMD python /root/src/server.py
