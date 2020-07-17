import App from './app';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import * as dotenv from 'dotenv';
import { EventEmitter } from 'events';
import ArbsController from './controllers/arbs/arbs.controller';
import ArbsListener from './listeners/arbs/arbs.listener';

dotenv.config();

if(!process.env.PORT)
    throw new Error('no port specified in config file');

// dependencies
const port: number = Number(process.env.PORT);
const arbsQueue = process.env.RABBITMQ_ARBS_QUEUE;
const arbsEventEmitter = new EventEmitter();

const app = new App({
    port: port, 
    controllers:[new ArbsController(arbsEventEmitter)],
    listeners:[new ArbsListener({queue: arbsQueue}, arbsEventEmitter)],
    middlewares:[
        helmet(),
        cors(),
        express.json()
    ]});

app.listen();