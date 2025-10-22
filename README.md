# Flask Transport UI ![build](https://github.com/williajm/flask_transport_ui/actions/workflows/python-app.yml/badge.svg)

This is a Flask learning project with a focus on testing.
The Flask application displays live train schedule information for UK train stations.
Autocomplete of the station name is via an AJAX call back to Flask.
Population of the live schedule information is via a websocket.
The live schedule information is provided by [transport api](https://www.transportapi.com/)
If you want to run this application with live data you need to sign up for a free application id and key [here](https://developer.transportapi.com/).
If you just want to see the application run use fake data with the ftu_fake_it env variable.

#### Setup

The simplest setup method is building and running a docker container.

docker build

```bash
docker build . -t ftu
```

docker run with live data

```bash
docker run -p 5000:5000 --env ftu_app_id=<app id> --env ftu_app_key=<app key> ftu
```

docker run with fake data (no transport credentials required)

```bash
docker run -p 5000:5000 --env ftu_fake_it="true" ftu
```

Or use docker compose

```bash
docker-compose up -d
```

You will then be able to access the application at http://127.0.0.1:5000/

##### Selenium Setup

To run against a dockerised Chrome you can use a docker network like:

```bash
docker network create grid
docker run -d -p 5000:5000 --env ftu_fake_it="true" --network="grid" --name test_server ftu
docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm --network="grid" selenium/standalone-chrome-debug
```

This also allows for a VNC sesssion on port 5900 to watch the tests.
