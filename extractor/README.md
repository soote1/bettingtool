# Extractor (Under development)
The extractor is a process manager that can:
* Start a list of different worker types.
* Stop the execution of a list of different worker types.

The extractor is configurable, it uses a json config file to define the set of workers to be managed.

The exctractor uses python's multiprocessing library to represent workers as different processes.

Each worker can be of one of the following types:
* **Url Seeder**: A stateful process that explores the betting websites to extract the odds URLs for each soccer match in a league.
* **Odds Fetcher**: An object that can fetch a web page from an url, extract the odds for a specific game type and generate a parsed output.
* **Url Consumer**: A process that establishes a connection with an URLs queue and waits for a new message to arrive. When a new message arrives, this process tells the fetcher to do his work and waits for the response. Once it gets a response from the fetcher, it sends a new message to the odds queue.
* **Url producer**: An object that can send urls to an URLs queue.
* **Odds producer**: An object that can send odds to an odds queue.

## Directory Structure
```python
├── docs               # documentation (TBD)
├── sample             # main package
    ├── caliente       # modules for getting odds data from caliente web site
        ├── cache      # cache management for caliente workers
        ├── model      # caliente models
        ├── workers    # caliente workers
    ├── common         # common utilities
        ├── cache      # classes for talking with redis
        ├── messaging  # classes for talking with rabbitmq
        ├── model      # classes for modeling odds data and workers
    ├── driver         # runnable script
    ├── manager        # process manager
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
