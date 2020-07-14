# Extractor
The extractor is a process manager that can:
* Create a set of objects recursively at runtime using reflection. These objects can represent a:
    * Worker.
    * Helper.
    * Dictionary.
* Create a list of processes and link them the corresponding worker object.
* Start a list of processes and run forever.
* Stop a list of processes when receiving a KeyboardInterrupt event.
* Terminate a list of processes after receiving a KeyboardInterrupt event.

The extractor is configurable, it uses a json config file to define the set of workers to be managed.

The exctractor uses python's multiprocessing library to represent workers as different processes.

A worker can either be:
* **Url Seeder**: A stateful process that explores the betting websites to extract the odds URLs for each game in a league.
* **Url Consumer**: A process that establishes a connection with a messaging system, hangs on a specific queue and waits for a new message to arrive. When a new message arrives, this process uses a helper to extract the odds from the received url, and another helper to send the odds to a specific queue.

A worker can use any of the following helpers:
* **Odds Fetcher**: An object that can fetch a web page from an url, extract the odds for a specific game type and generate a parsed output.
* **Url producer**: An object that can send urls to an URLs queue.
* **Odds producer**: An object that can send odds to an odds queue.

See the [Extractor Design](https://github.com/soote1/bettingtool/wiki/Design-%7C-Extractor) for more details.

## Directory Structure
```python
├── docs               # documentation (TBD)
├── sample             # main package
    ├── caliente       # modules for getting odds data from caliente web site
        ├── cache      # cache management for caliente workers
        ├── workers    # caliente workers
    ├── common         # common utilities
        ├── cache      # classes for talking with redis
        ├── helpers    # helpers to be shared across packages
        ├── model      # classes for modeling odds metadata
    ├── main           # entry point
├── tests              # unit tests package (TBD)
```

## Dependencies

The extractor project supports pipenv for dependency management.

Run:
```python
pipenv install
```
to install the following dependencies:
```python
* pytest: unit tests
* beautifulsoup4: web crawling
* walrus: redis client
* requests: http communication
* lxml: parser used by beautifulsoup
* pika: rabbitmq client
```
