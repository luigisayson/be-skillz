from python:3
COPY . .
RUN pip install -r requirements.txt
CMD ["make", "default-run"]
