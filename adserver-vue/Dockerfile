FROM ubuntu:18.04

RUN apt-get update && apt-get install -y gcc node.js npm

WORKDIR ./vue-app

ADD . /vue-app/

RUN npm install webpack-dev-server@2.9.7 --save-dev

CMD npm run watch
