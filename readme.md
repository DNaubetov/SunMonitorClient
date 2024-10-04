docker build -t sun-monitor-client .
docker run -d --env-file .env --restart always sun-monitor-client
