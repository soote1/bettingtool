import { Application } from 'express';
import express from 'express';
import AppConfig from './interfaces/app-config';
import IControllerBase from './interfaces/controller-base.interface';
import IListenerBase from './interfaces/listener-base.interface';

export default class App {
    public app: Application;
    public port: number;

    /**
     * Initialize the application using a configuration object
     * @param appConfig 
     */
    constructor(appConfig: AppConfig) {
        this.app = express();
        this.port = appConfig.port;

        this.loadControllers(appConfig.controllers);
        this.loadMiddlewares(appConfig.middlewares);
        this.startListeners(appConfig.listeners);
    }

    /**
     * Registers a list of middlewares on the express app
     * @param middlewares 
     */
    private loadMiddlewares(middlewares: any[]) {
        middlewares.forEach(middleware => this.app.use(middleware));
    }

    /**
     * Registers a list of controllores on the express app
     * @param controllers 
     */
    private loadControllers(controllers: IControllerBase[]) {
        controllers.forEach(controller => this.app.use('/', controller.router));
    }

    /**
     * Starts a list of listeners
     * @param listeners 
     */
    private startListeners(listeners: IListenerBase[]) {
        listeners.forEach(listener => listener.start());
    }

    /**
     * Starts listening for requests
     */
    public listen() {
        this.app.listen(this.port, () => {
            console.log(`App listening on port ${this.port}`);
        });
    }
}