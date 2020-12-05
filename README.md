# x12GenApp
Integrates X12 Transactions with IBM's General Insurance Application on Z Systems.

## Overview
x12GenApp provides a simple REST based API capable of integrating X12 transactions with the General Insurance Application's APIs. 
A single endpoint is used to consume x12 transactions. Specific transaction handling is implemented by parsing the transaction's `ST` segment and processing accordingly.

The request format consists of a single key, x12, and the corresponding x12 payload.
```shell script
HTTP 1.1
Accept: application/json
Content-Type: application/json

{
  "x12": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145<etc>"
}
```

The response uses the same format as the request.
```shell script
HTTP 1.1
Content-Type: application/json

{
  "x12": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145<etc>",
  "x12_transaction_code": "271"
}
```

OpenAPI documentation is available at `http://<host>/docs`

Transaction sets supported include:
- 270/271 for Insurance Eligibility Verification

## Endpoints
| Endpoint | Description |
| -------- | ----------- |
| http://<host>:8080/docs | OpenAPI documentation |
| http://<host>:8080/x12 | The X12 message POST endpoint |

## Eligibility Check (270/271) Processing
The eligibility check processing workflow consists of the following steps:
- An API Client submits a X12 270 transaction to the x12GenApp endpoint genapp/x12 [POST]
- The endpoint parses member demographics from the X12 transaction for use in a GenApp Customer Search
- The 271 response transaction returned indicates the member is covered if match is found. Otherwise the member does not have coverage.

Demographics from the X12 270 transaction are returned in the X12 271 transaction to provide a meaningful response.

## Installing For Local Development
A local development environment requires Python 3.x or higher.

Create the local development environment within a terminal (Linux based systems) or PowerShell (Windows)
```
cd <desired project base directory>
git clone <project url>
cd <project directory>
python3 -m venv env
```

Activate the project's virtual environment . . . 
On Windows
```
env\Scripts\activate
```

On Linux based systems
```
source env\bin\activate
```

Link the development code to the virtual environment and run tests
```
pip install -e . .[test]
pytest
```

## Container Support
Build and run the container image
```
docker build -t x12genapp .
docker run --rm --name x12genapp -p 8080:80 -d x12genapp
```
