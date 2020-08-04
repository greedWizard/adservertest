FROM node:12.16.1

RUN mkdir ./vue-app

WORKDIR /vue-app

ENV PATH /vue-app/node_modules/.bin:$PATH

ADD package.json /app/package.json

RUN npm config set registry http://registry.npmjs.org/ && npm install

RUN npm install --save-dev webpack webpack-cli  && npm install webpack-dev-server -g && npm link webpack && npm link webpack-cli

ADD . /vue-app

RUN npm install

CMD npm run dev
