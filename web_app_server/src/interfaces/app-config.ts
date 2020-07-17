import IControllerBase from "./controller-base.interface";
import IListenerBase from "./listener-base.interface";

export default interface AppConfig {
    port: number;
    controllers: IControllerBase[];
    listeners: IListenerBase[];
    middlewares: any[];
}