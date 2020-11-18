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
Transaction sets supported include:
- 270/271 for Insurance Eligibility Verification

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
python3 -m venv env
```

Activate the virtual environment . . . 
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
Coming soon!