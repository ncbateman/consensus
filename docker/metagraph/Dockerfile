FROM consensus-base:latest

COPY ./src/consensus/metagraph/metagraphcron /etc/cron.d/metagraphcron
RUN chmod 0644 /etc/cron.d/metagraphcron && crontab /etc/cron.d/metagraphcron

COPY ./src/consensus/metagraph/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]