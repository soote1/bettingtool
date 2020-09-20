FROM node:current

WORKDIR /dashboard

ADD ./dashboard/ .
ADD ./wait-for-it.sh .

RUN npm install

CMD ["ng", "serve"]