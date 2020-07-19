import IControllerBase from '../../interfaces/controller-base.interface';
import { Router, Request, Response } from 'express';
import express from 'express';
import { EventEmitter } from 'events';

export default class ArbsController implements IControllerBase {
    router: Router;
    path: string;
    arbsEventEmitter: EventEmitter;

    constructor(arbsEventEmitter: EventEmitter) {
        this.path = '/arbs';
        this.arbsEventEmitter = arbsEventEmitter;
        this.router = express.Router();
        this.initRoutes();
    }

    /**
     * Loads a set of route handlers on the app router
     */
    initRoutes(): void {
        this.router.get(this.path, this.emitArbs);
    }

    /**
     * A route handler for sending arbs to the clients using
     * Server Sent Events
     * @param req 
     * @param res 
     */
    emitArbs = async(req: Request, res: Response) => {
        try {
            console.log('Client connected to arbs streaming');
    
            // set headers
            res.set('Content-Type', 'text/event-stream');
            res.set('Connection', 'keep-alive');
            res.set('Cache-Control', 'no-cache');
            res.set('Access-Control-Allow-Origin', '*');
    
            // subscribe to push event
            this.arbsEventEmitter.on('arbs-received', (event, data) => {
                console.log('[ArbsController] Pushing arbs to client');
                res.write('event: ' + String(event) + '\n' + 'data: ' + data + '\n\n');
            });
        }
        catch(e) {
            res.status(404).send(e.message);
        }
    }
}