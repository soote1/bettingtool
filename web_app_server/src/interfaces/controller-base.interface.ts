import { Router } from 'express';

export default interface IControllerBase {
    router: Router;
    path: string;
    
    initRoutes(): void;
}