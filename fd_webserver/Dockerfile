FROM aibasel/downward:21.12

# HACK: http://stackoverflow.com/questions/25193161/chfn-pam-system-error-intermittently-in-docker-hub-builds
RUN ln -s -f /bin/true /usr/bin/chfn

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3-pip python3 build-essential curl gcc g++ make g++-multilib

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -

RUN apt-get install -y nodejs 

RUN pip3 install Flask
RUN npm install -g webpack@3.11.0 yarn

COPY ./fd_webserver /fastdownward
WORKDIR /fastdownward

RUN yarn add node-sass
RUN yarn && yarn run production

ENTRYPOINT []
CMD bash -c "python3 app.py"
