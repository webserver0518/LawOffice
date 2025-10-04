FROM python:3.11-slim
LABEL authors="matan"
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "run.py"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]