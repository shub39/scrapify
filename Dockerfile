FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY scraper.py .
COPY data.csv .
COPY .env .

RUN pip install discord.py python-dotenv requests beautifulsoup4

CMD ["python3", "main.py"]
