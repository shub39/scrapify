FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY scraper.py .
COPY data.csv .
COPY .env .
COPY DS_DATA.ods .

RUN pip install discord.py python-dotenv requests beautifulsoup4 pyexcel pyexcel-ods3 pyexcel-odsr

CMD ["python3", "main.py"]
