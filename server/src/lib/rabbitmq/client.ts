import amqp from 'amqplib';

export default class RabbitMQClient {
    // Create singleton instane
    private static _instance: RabbitMQClient = new RabbitMQClient();

    // RabbitMQ communication
    private connection;
    private channel;

    // TODO: Do we want to support multiple handlers on each queue?
    private queues = {};

    /**
     * Create a new instance and assign it to the _instance property.
     * Avoid the usage when the variable has been initialized for the
     * first time.
     */
    constructor() {
        if(RabbitMQClient._instance) {
            throw new Error('An instance for this class already exist... use getInstance() method');
        }

        this.initConnection();
        RabbitMQClient._instance = this;
    }

    /**
     * Initialize connection to rabbitmq server
     */
    async initConnection() {
        this.connection = await amqp.connect(process.env.RABBITMQ_CONNECTION_STRING);
        this.channel = await this.connection.createChannel();
    }

    /**
     * Send a message to a specific queue
     */
    async send(queue, message) {
        if(!this.connection) {
            await this.initConnection();
        }

        await this.channel.assertQueue(queue, {durable:true});
        this.channel.sendToQueue(queue, message);
    }

    /**
     * Consume messages from a given queue and handle them using
     * a given handler function.
     * @param queue 
     * @param handler 
     * @param handlerArgs 
     */
    async subscribe(queue, handler, handlerArgs = undefined) {
        if(!this.connection) {
            await this.initConnection();
        }

        await this.channel.assertQueue(queue, {durable:true});
        this.channel.consume(
            queue,
            async(message) => {
                // handle message
                if(handlerArgs) {
                    handler(message, handlerArgs);
                }
                else {
                    handler(message);
                }
                // remove channel from queue
                this.channel.ack(message);
            }
        );
    }

    /**
     * Get client instance
     */
    static async getInstance() {
        return RabbitMQClient._instance;
    }
}