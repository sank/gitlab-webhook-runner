FROM python:3.6-onbuild
RUN python setup.py install

COPY docker.ini /opt/gitlab-webhook-runner/docker.ini
COPY docker_entrypoint_script.sh /opt/gitlab-webhook-runner/docker_entrypoint_script.sh
COPY docker_script.sh /opt/gitlab-webhook-runner/docker_script.sh
WORKDIR /opt/gitlab-webhook-runner

EXPOSE 6543
RUN apt-get update
RUN apt-get install sshpass
CMD ["pserve", "docker.ini"]
