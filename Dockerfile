FROM python:3.10

WORKDIR /app

COPY requirements1.txt .
RUN ["pip", "install", "-r", "requirements1.txt"]

COPY requirements2.txt .
RUN ["pip", "install", "--force-reinstall", "-r", "requirements2.txt"]

COPY requirements3.txt .
RUN ["pip", "install", "-r", "requirements3.txt"]
RUN ["playwright", "install"]

COPY . .

EXPOSE 8000
CMD ["sh", "start.sh"]