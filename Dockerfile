FROM  python:3.7.17-slim-bullseye as installer
ENV MULTIDICT_NO_EXTENSIONS=1

WORKDIR /opt/i5k
COPY  src/package* src/*.js ./
RUN apt-get -qq update --fix-missing && \
    apt-get --no-install-recommends -y install npm gcc libz-dev libjpeg-dev libpcre3 libpcre3-dev && \
    npm install && \
    rm package*

FROM  python:3.7.17-slim-bullseye as builder
ARG APP_HOME=/opt/i5k
ARG APP_USER=i5k
ARG UID
ARG GID
WORKDIR ${APP_HOME}
ENV MULTIDICT_NO_EXTENSIONS=1
COPY . .
COPY --from=installer ${APP_HOME} ./src/

RUN groupdel -f  dialout  && \
    apt-get -qq update --fix-missing && \
    apt-get --no-install-recommends -y install direnv supervisor nginx gcc libz-dev libjpeg-dev libpcre3 libpcre3-dev && \
    pip3 install --upgrade pip poetry && \
    groupadd -o -f -g ${GID} ${APP_USER} && \
    useradd -g ${GID} -u ${UID} -M -d ${APP_HOME} -c "${APP_USER} Application User" -s /bin/bash ${APP_USER} && \
    mv docker-files/nginx.conf /etc/nginx/nginx.conf && \
    mv docker-files/default.conf /etc/nginx/sites-available/default && \
    sed -i "s|APP_HOME|${APP_HOME}|g" /etc/nginx/nginx.conf  /etc/nginx/sites-available/default && \
    chown -R ${APP_USER}:${APP_USER} ${APP_HOME} /etc/nginx /var/lib/nginx /var/log/nginx && \
    rm src/package*


FROM  builder as app
ARG APP_HOME=/opt/i5k
ARG APP_USER=i5k
ARG UID
ARG GID
WORKDIR ${APP_HOME}
ENV MULTIDICT_NO_EXTENSIONS=1
USER ${APP_USER}
RUN mkdir -p production media .venv run logs src/static  && \
    mv docker-files/envrc .envrc && mv docker-files/direnvrc .direnvrc && \ 
    poetry install && mv docker-files/*.sh ${APP_HOME}/.venv/bin/ && \
    mv src/manage.py production/ && \
    mv docker-files/supervisord.conf ./ && mv docker-files/appenvrc production/.envrc && \
    ln -s ${APP_HOME}/src/* production/ && \
    echo 'eval "$(direnv hook bash)"' >> ${APP_HOME}/.bashrc && \
    bash -c "cd ${APP_HOME} && direnv allow . " && \ 
    bash -c "cd ${APP_HOME}/production && direnv allow  ." && \
    cp -R production training && \
    tee  production/i5k.ini training/i5k.ini < docker-files/i5k.ini && rm docker-files/i5k.ini && \
    sed -i "s|APP_USER|${APP_USER}|g;s|APP_DIR|${APP_HOME}|g " production/i5k.ini training/i5k.ini  && \
    sed -i "s|APP_ID|production|g;s|APP_HOME|${APP_HOME}/production/|g  " production/i5k.ini && \
    sed -i "s|APP_ID|training|g;s|APP_HOME|${APP_HOME}/training/|g " training/i5k.ini && \
    sed -i "s|APP_HOME|${APP_HOME}|g" supervisord.conf ${APP_HOME}/.venv/bin/startapp.sh && \
    sed -i 's|_training||g' production/.envrc && \
    chmod +x ${APP_HOME}/.venv/bin/*.sh && \
    chmod -R o-rwx ${APP_HOME} && \
    cd ${APP_HOME}/production && direnv allow . && \
    ${APP_HOME}/.venv/bin/python3 ./manage.py collectstatic --no-input -c -v 3 && \
    cd ${APP_HOME}/training && direnv allow . && \
    rmdir ${APP_HOME}/docker-files

    ENTRYPOINT ["/opt/i5k/.venv/bin/entry-point.sh"]