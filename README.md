# Client

### About

Flask api that provides interaction with a raspberry pi's GPIO interface through HTTP requests.

### Requirements

##### Python packages
* flask
* flask-classy
* supervisor

### Configuration

Requires a config file named `camserv.conf` located in the root directory of the repository.  An example config is shown below.

```
[pins]
17=green
22=yellow
23=red
```