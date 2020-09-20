FROM node:current

WORKDIR /server

ADD ./server/ .
ADD ./wait-for-it.sh .

RUN npm install

CMD ["npm", "run", "build-and-start"]