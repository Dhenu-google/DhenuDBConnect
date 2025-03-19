FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

ENV PORT 8080

EXPOSE 8080

WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]