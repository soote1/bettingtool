/**
 * Initial script for:
 * - consuming data from a rabbitmq queue
 * - sending the data to the browser using server sent events pattern
 * 
 * A refactor to improve the code quality is needed
 */
const Express = require('express');
const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');
let amqp = require('amqplib/callback_api');

const app = Express();
const eventEmitter = new EventEmitter();

app.get('/', (req, res) => {
    res.status(200).send('x');
});

// server sent events connection
app.get('/sse', (req, res) => {
    console.log('Client connected to sse');

    // set headers
    res.set('Content-Type', 'text/event-stream');
    res.set('Connection', 'keep-alive');
    res.set('Cache-Control', 'no-cache');
    res.set('Access-Control-Allow-Origin', '*');

    // subscribe to push event
    eventEmitter.on('push', (event, data) => {
        res.write('event: ' + String(event) + '\n' + 'data: ' + data + '\n\n');
    });
});

// create rabbitmq consumer
let connectionString = 'amqp://localhost';
amqp.connect(connectionString, (connectionError, connection) => {
    if(connectionError) {
        throw connectionError;
    }

    connection.createChannel((channelError, channel) => {
        if(channelError) {
            throw channelError;
        }

        let queue = 'caliente_odds_queue';
        let queueOptions = {durable:true};
        channel.assertQueue(queue, queueOptions);
        console.log('[*] Waiting for messages in %s. Press Ctrl+C to exit.', queue);
        channel.consume(queue, (message) => {
            eventEmitter.emit("push", "some-event", message.content.toString());
        }, {noAck: true});
    });
});

app.listen(1234, (err) => {
    if(err) {
        console.log('Server can not listen');
        return;
    }
    console.log('Server is listening');
})