FROM jbarlow83/ocrmypdf

COPY server.py /server.py
ENTRYPOINT ["python3", "/server.py"]
