import IListenerBase from '../../interfaces/listener-base.interface';
import RabbitMQClient from '../../lib/rabbitmq/client';
import { EventEmitter } from 'events';

export default class ArbsListener implements IListenerBase {
    queue: string;
    arbsEventEmitter: EventEmitter;

    constructor(config, arbsEventEmitter) {
        this.queue = config.queue;
        this.arbsEventEmitter = arbsEventEmitter;
    }

    start() {
        RabbitMQClient.getInstance().then(client => {
            console.log('[ArbsListener] arbs listener started... waiting for messages');
            client.subscribe(this.queue, this.handleMessages, this.arbsEventEmitter);
        });
    }

    handleMessages(message, arbsEventEmitter) {
        console.log('[ArbsListener] arbs received');
        arbsEventEmitter.emit('arbs-received', 'arb-found', message.content.toString());
    }
}