export default interface RabbitMQConfig {
    connectionString: string;
    queue: string;
    queueOptions: any
}