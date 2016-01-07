Argus
=====
Argus enables you to watch file system events through web sockets.

### Settings

Argus can be customized by running it with custom enviroment variables. The different settings and their default values can be found in [`settings.py`](argus/argus/settings.py).

## Deploying Argus

Deploying Argus is done with Docker Compose. All you have to do is create a `docker-compose.yml` file and then run `docker-compose up`. To make your life easier, instead of writing the whole `docker-compose.yml` you can use [`docker-compose-base.yml`](docker-compose-base.yml) and extend its services according to your needs ([example file](examples/docker-compose.yml)).

## License
Argus is licensed under the MIT License. More info at [LICENSE](LICENSE) file.
