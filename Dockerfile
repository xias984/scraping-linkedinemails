FROM python:3.12.3
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y supervisor && rm -rf /var7lib/ant/lists/*
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 9001
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]