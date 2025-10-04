FROM python:3.11-slim
LABEL authors="matan"

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

#CMD ["python", "run.py"]
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]