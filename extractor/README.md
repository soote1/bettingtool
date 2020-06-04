# Extractor (Under development)
The extractor is a process manager. It manages the execution of a set of workers.

The workers can have one of the following types:
* Url Seeder: A stateful process that explores the betting websites to extract the odds URLs.
* Odds Fetcher: An object that can fetch a web page from an url, extract the odds and create a parsed output.
* Url Consumer: A process that establishes a connection with an URLs queue and waits for a new message to arrive. When a new message arrives, this process tells the fetcher to do his work and waits for the response. Once it gets a response from the fetcher, it sends a new message to the odds queue.

The extractor is configurable, it uses a json file to prepare the set of workers.

## Directory Structure
```python
├── docs               # documentation (TBD)
├── sample             # main package
    ├── cache          # classes for talking with redis
    ├── caliente       # classes for getting odds data from caliente web site
    ├── config         # the extractor configuration
    ├── messaging      # classes for talking with rabbitmq
    ├── model          # classes for modeling odds data
    ├── workers        # abstract worker classes to be used for each betting web site package
├── tests              # unit test package (TBD)
```

## Dependencies

The extractor project supports pipenv for dependency management.

* pytest: unit tests
* beautifulsoup4: web crawling
* walrus: redis client
* requests: http communication
* lxml: parser used by beautifoulsoup
* pika: rabbitmq client