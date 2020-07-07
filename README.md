# Gorila Back-end

## Requirements

- Docker

## How to run locally

```
git clone https://github.com/tsuhadaniel/gorila-test.git
cd gorila-test/

sudo docker build . -t gorila/test
sudo docker run -it -p 5000:5000 gorila/test
```
Go to http://localhost:5000/

## How to run tests

```
sudo docker run -it gorila/test /bin/bash

# inside docker
eval "$($HOME/miniconda/bin/conda shell.bash hook)" \
&& conda activate simple-server \
&& python -m unittest
```

## API

### Parameters:

- investmentDate (YYYY-MM-DD)
- currentDate (YYYY-MM-DD)
- cdbRate (Float)

### Via GET

```
curl -X GET -i 'http://localhost:5000/api?investmentDate=2016-11-14&currentDate=2016-12-26&cdbRate=103.5'
```

### Via POST

```
curl -X POST \
-H 'Content-Type: application/json' \
-i http://localhost:5000/api \
--data '{"investmentDate":"2016-11-14","cdbRate":103.5,"currentDate":"2016-12-26"}'
```
