# Flask Transport UI

This is a Flask learning project.   
The Flask application displays live train schedule information for UK train stations.  
Autocomplete of the station name is via an AJAX call back to Flask.  
Population of the live schedule information is via a websocket.    
The live schedule information if provided by [transport api](https://www.transportapi.com/)  
If you want to run this application with live data you need to sign up for a free application id and key [here](https://www.transportapi.com/plans/).   
If you just want to see the application run use fake data with the ftu_fake_it env variable.

#### Setup

The simplest setup method is building and running a docker container.  

docker build
```console
docker build . -t ftu
```

docker run with live data
```console
docker run -p 5000:5000 --env ftu_app_id=<app id> --env ftu_app_key=<app key> ftu  
```

docker run with fake data (no transport credentials required)
```console
docker run -p 5000:5000 --env ftu_fake_it="true" ftu  
```

You will then be able to access the application at http://127.0.0.1:5000/
