# x12GenApp
Integrates X12 Transactions with IBM's General Insurance Application on Z Systems.

## Overview
x12GenApp provides a simple REST based API capable of integrating X12 transactions with the General Insurance Application's APIs. 
A single endpoint is used to consume x12 transactions. Specific transaction handling is implemented by parsing the
transaction's `ST` segment and to determine the transaction format which selects the rules (eligibility, claims, 
enrollment, etc) used to parse the transaction set.

The x12 endpoint parses membership data from the x12 transaction for use in a Genapp customer lookup. The lookup executes
against a record cache which is built when the application starts. The lookup may be bypassed using the
`is_passthrough_enabled` configuration setting. When the lookup is bypassed, an "affirmative" x12 response is returned
based on the input data. For example a 270 transaction submitted when `is_passthrough_enabled` is True will return a
271 transaction with member coverage information.

The request format consists of a single key, x12, and the corresponding x12 payload.
```shell script
HTTP 1.1
Accept: application/json
Content-Type: application/json

{
  "x12": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145<etc>"
}
```

The response includes the x12 response transaction with the x12 transaction code.
```shell script
HTTP 1.1
Content-Type: application/json

{
  "x12": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145<etc>",
  "x12_transaction_code": "271"
}
```

Transaction sets supported include:
- 270/271 for Insurance Eligibility Verification

## Configuration
Application settings are defined in a configuration class, [AppSettings](x12genapp/config.py)

| Setting                | Description                                                                                      | Default                     |
| ---------------------- | -------------------------------------------------------------------------------------------------| --------------------------- |
| uvicorn_app            | Path (python module and attribute) to the FastAPI application                                    | x12genapp.main:app          |
| uvicorn_host           | Specifies the host/binding address for the FastAPI application                                   | 0.0.0.0                     |
| uvicorn_port           | The port the FastAPI application's listening port                                                | 8080                        |
| uvicorn_reload         | Set to True to support hot-reload for local debugging                                            | False                       |
| is_passthrough_enabled | Set to True to bypass the Genapp Customer lookup, which returns an "affirmative" x12 transaction | False                       |
| genapp_base_url        | The base Genapp url including protocol, host, port, and app root                                 | http://localhost:9990/Genapp|
| genapp_customer_lookup | The Genapp customer lookup endpoint                                                              | /Customer/Ing               |
| genapp_customer_min_id | Specifies the first record included in the Genapp customer cache                                 | 1                           |
| genapp_customer_max_id | Specifies the last record included in the Genapp customer cache                                  | 5                           |

Settings are configured using [FastAPI's implementation](https://fastapi.tiangolo.com/advanced/settings/) which is based
on [Pydantic's Setting implementation](https://fastapi.tiangolo.com/advanced/settings/).

Settings are overriden using environment variables prior to launching the application.
```shell
export IS_PASSTHROUGH_ENABLED=True
python3 x12genapp/main.py
```

## Endpoints
| Endpoint | Description |
| -------- | ----------- |
| http://<host>:8080/docs      | OpenAPI documentation |
| http://<host>:8080/x12       | The X12 message POST endpoint |
| http://<host>:8080/customers | Returns cached Genapp customer records |

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
pip3 install --upgrade pip
pip3 install -e .[test]
# note on OS X if zsh is the default shell the command will need to be quoted 
#pip3 install -e '.[test]'

pytest
```

## Container Support
Build and run the container image
```
docker build -t x12genapp .
docker run --rm --name x12genapp -p 8080:80 -d x12genapp
```
