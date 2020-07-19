Table of Contents
=======================

* [What is bettingtool?](#what-is-bettingtool)
* [Supported Online Sports Betting Sites](#supported-online-sports-betting-sites)
* [Installation Instructions](#installation-instructions)
* [Running bettingtool](#running-bettingtool)
* [Testing](#testing)
* [Community and Contributing](#community-and-contributing)
* [Directory Structure](#directory-structure)
* [Licensing](#licensing)

---

What is bettingtool?
------
bettingtool is an open source odds analysis system. It follows an event processing architecture to perform the following tasks:

* Extract the odds for different types of bets in a game from online sports betting sites.
* Emit the odds so that event processors can analyze and produce outcomes.
* Consume the odds and process them using a multi-objective genetic algorithm to search for an arbitrage opportunity.
* Emit the arbitrage opportunity when it is found by an event processor.
* Consume the arbitrage opportunities and loads them on a dashboard for real-time monitoring.

Supported online sports betting sites.
------
Currently, bettingtool supports data extraction for the following online betting sites:

* Caliente.

Support for more online sports betting sites coming soon.

Installation Instructions
------
* Install RabbitMQ (extractor, processor, web app server, pythontools): https://www.rabbitmq.com/download.html
* Install Redis (extractor): https://redis.io/download
* Install Python 3 (extractor, processor, pythontools): https://www.python.org/downloads/
* Install pipenv (extractor, processor, pythontools): https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv
* Install NodeJs and NPM (web app server): https://nodejs.org/es/

Docker file coming soon.

Running bettingtool
------
To start the bettingtool components you will need to have the following processes running:
* Local redis instance listening on port 6379 (default).
* Local rabbitmq server instance listening on port 5672 (default).

Start the extractor:
```python
python -m extractor.sample.main
```

Start the processor:
```python
python -m processor.sample.main
```

Start the web app server:
* Install dependencies first:
```javascript
npm install
```
* On a terminal:
```javascript
npm run webpack
```
* On a different terminal:
```javascript
npm start
```

Start the web app client. (Pending)

Testing
------
Currently, bettingtool supports basic unit tests for several components such as the extractor, processor, and pythontools. You can run them using pytest framework (https://docs.pytest.org/en/stable/getting-started.html).

Steps:

* From the root directory of any component mentioned in the above section, cd to the "tests" folder.
* Run the pytest command.

The goal is to support both unit and integration testing for all the components involved in the system.

Community and Contributing
------
Contributions are welcome. Check out the [Contribution Guide](CONTRIBUTING.md).

Directory Structure
------
```python
├── extractor                   # Process manager for the web crawlers.
├── processor                   # Process manager for the processing enginges.
├── pythontools                 # Common logic for the extractor and the processor.
├── server                      # Http server for pushing real-time data to the UI.
├── web_app_UI                  # UI to visualize the events produced by the processor.
```

Licensing
------
The code in this project is released under the [MIT License](LICENSE).