# Configurations

This documentation provides an overview of the configurations required for the
project. It includes information on requirements, dependencies, installation,
usage, Docker, Docker Compose, logging, and FAQs.

## Table of Contents

1. [Requirements](#requirements)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Environment Variables](#environment-variables)
5. [Usage](#usage)
   - [Start API](#start-api)
6. [Docker](#docker)
   - [Build](#build)
   - [Run](#run)
7. [Docker Compose](#docker-compose)
8. [Logging](#logging)
   - [Python](#python)
   - [Docker](#docker-1)
9. [FAQs](#faqs)

## Requirements

Before proceeding with the installation and usage of the project, ensure that
the following requirements are met:

- [Python](https://www.python.org/) (version >=
  [3.8.10](https://www.python.org/downloads/release/python-3810/))
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Dependencies

The project has certain dependencies that need to be installed. On Ubuntu, run
the following command to install the required dependencies:

```bash
$ sudo apt install python3-dev libmysqlclient-dev apache2 apache2-dev make libapache2-mod-wsgi-py3
```

## Installation

To install the project, follow these steps:

1. Create a virtual environment:

   ```bash
   $ python3 -m venv venv
   $ . venv/bin/activate
   ```

2. Install the required packages:

   ```bash
   $ pip install -r requirements.txt
   ```

## Environment Variables

The project utilizes several environment variables for configuration. These
variables control various aspects of the project's behavior. The following table
provides an overview of the available environment variables:

| Variable                | Description                                                                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HOST`                  | The host address to bind the API.                                                                                                                  |
| `PORT`                  | The port number on which the API will listen for incoming requests.                                                                                |
| `SSL_SERVER_NAME`       | The server name for SSL configuration.                                                                                                             |
| `SSL_PORT`              | The port number for SSL configuration.                                                                                                             |
| `SSL_CERTIFICATE`       | The path to the SSL certificate file. Required for HTTPS communication.                                                                            |
| `SSL_KEY`               | The path to the SSL private key file. Required for HTTPS communication.                                                                            |
| `SSL_PEM`               | The path to the SSL certificate chain file. Required for HTTPS communication.                                                                      |
| `SSL_FILE_PATH`         | The path to the directory containing SSL certificate and key files. Required for HTTPS communication.                                              |
| `WHATSAPP_CREDENTIALS`  | JSON-formatted array containing WhatsApp API credentials. Each object should contain `access_token`, `phone_number_id`, and `phone_number` fields. |
| `WHATSAPP_VERIFY_TOKEN` | The verify token for WhatsApp API authentication.                                                                                                  |
| `WEBHOOK_URLS`          | JSON-formatted array containing webhook URLs to receive incoming messages.                                                                         |
| `MODE`                  | The mode in which the server operates (`production`, `development`, etc.).                                                                         |

> **Note:** The values for these variables should be provided according to your
> specific configuration requirements.

You can set these environment variables in different ways, depending on your
deployment setup, such as directly in the command line, using a `.env` file, or
within a container orchestration system like Dokcer and Docker Compose.

To learn how to set the environment variables, please refer to the [FAQs](#faqs)
section of the documentation.

## Usage

### Start API

To start the API, you have two options: using Python directly or using MOD_WSGI.

**Using Python**

```bash
$ HOST= \
  PORT= \
  SSL_SERVER_NAME= \
  SSL_PORT= \
  SSL_CERTIFICATE= \
  SSL_KEY= \
  SSL_PEM= \
  WHATSAPP_CREDENTIALS='[{"access_token":"", "phone_number_id":"", "phone_number":""}]' \
  WHATSAPP_VERIFY_TOKEN= \
  WEBHOOK_URLS='[]' \
  MODE=production \
  python3 server.py
```

**Using MOD_WSGI**

```bash
$ HOST= \
  PORT= \
  SSL_SERVER_NAME= \
  SSL_PORT= \
  SSL_CERTIFICATE= \
  SSL_KEY= \
  SSL_PEM= \
  WHATSAPP_CREDENTIALS='[{"access_token":"", "phone_number_id":"", "phone_number":""}]' \
  WHATSAPP_VERIFY_TOKEN= \
  WEBHOOK_URLS='[]' \
  MODE=production \
  mod_wsgi-express start-server wsgi_script.py \
  --user www-data \
  --group www-data \
  --port '${PORT}' \
  --ssl-certificate-file '${SSL_CERTIFICATE}' \
  --ssl-certificate-key-file '${SSL_KEY}' \
  --ssl-certificate-chain-file '${SSL_PEM}' \
  --https-only \
  --server-name '${SSL_SERVER_NAME}' \
  --https-port '${SSL_PORT}'
```

## Docker

### Build

To build the Docker image for the project, use the following commands:

```bash
$ docker build --target development -t smswithoutborders-customplatform-whatsapp .
```

```bash
$ docker build --target production -t smswithoutborders-customplatform-whatsapp .
```

### Run

To run the Docker image for the project, use the following commands:

**Development Image:**

```bash
$ docker run -d -p 17000:17000 \
  --name smswithoutborders-customplatform-whatsapp \
  --env 'HOST=' \
  --env 'PORT=' \
  --env 'WHATSAPP_CREDENTIALS=[{"access_token":"", "phone_number_id":"", "phone_number":""}]' \
  --env 'WHATSAPP_VERIFY_TOKEN=' \
  --env 'WEBHOOK_URLS=[]' \
  smswithoutborders-customplatform-whatsapp
```

**Production Image:**

```bash
$ docker run -d -p 17000:17000 \
  --name smswithoutborders-customplatform-whatsapp \
  --env 'HOST=' \
  --env 'PORT=' \
  --env 'SSL_SERVER_NAME=' \
  --env 'SSL_PORT=' \
  --env 'SSL_CERTIFICATE=' \
  --env 'SSL_KEY=' \
  --env 'SSL_PEM=' \
  --env 'WHATSAPP_CREDENTIALS=[{"access_token":"", "phone_number_id":"", "phone_number":""}]' \
  --env 'WHATSAPP_VERIFY_TOKEN=' \
  --env 'WEBHOOK_URLS=[]' \
  smswithoutborders-customplatform-whatsapp
```

> Note: You can also read environment variables from a file using the
> `--env-file` command. For example:

```bash
$ docker run -d -p 17000:17000 \
  --name smswithoutborders-customplatform-whatsapp \
  --env-file .env \
  smswithoutborders-customplatform-whatsapp
```

## Docker Compose

To run the project using Docker Compose, follow these steps:

1. Ensure that you have filled in all the necessary environment variables.
2. Use the following command:

```bash
$ docker compose \
  -e 'HOST=' \
  -e 'PORT=' \
  -e 'SSL_SERVER_NAME=' \
  -e 'SSL_PORT=' \
  -e 'SSL_FILE_PATH=' \
  -e 'SSL_CERTIFICATE=' \
  -e 'SSL_KEY=' \
  -e 'SSL_PEM=' \
  -e 'WHATSAPP_CREDENTIALS=[{"access_token":"", "phone_number_id":"", "phone_number":""}]' \
  -e 'WHATSAPP_VERIFY_TOKEN=' \
  -e 'WEBHOOK_URLS=[]' \
  up -d
```

> Note: You can also read environment variables from a file using the
> `--env-file` command. For example:

```bash
$ docker compose --env-file .env up -d
```

## Logging

### Python

To start the Python server with logging enabled, use the following command:

```bash
$ python3 server.py --logs=debug
```

### Docker

To view the container logs, use the following command:

```bash
$ docker logs smswithoutborders-customplatform-whatsapp
```

## FAQs

**Q: How can load environment variables from a `.env file` and set them as the
default bash environment variables?**

A: You can use the following command to copy the `env.example` file to `.env`:

```bash
$ cp env.example .env
```

Then, open the `.env` file and modify the values to match your requirements.
Finally, set the environment variables as the default bash environment variables
using the following command:

```bash
$ source .env
```

or

```bash
$ export $(cat .env)
```

This will load the environment variables defined in the `.env` file into the
current shell session.

**Q: How can I obtain my WhatsApp API access token and phone number ID?**

A: Follow these steps to obtain your WhatsApp API access token and phone number
ID:

1. Visit the [Meta developers apps](https://developers.facebook.com/apps) page.
2. Create a new app by clicking on the
   [Create](https://developers.facebook.com/apps/create/) button.
3. Choose the "Business" option.
4. Provide the required basic app information.
5. Locate WhatsApp Messenger (usually found at the bottom of the list) and add
   it to your app.
6. In the left sidebar, navigate to `WhatsApp` and then `API Setup` You will
   find your TOKEN, TEST WHATSAPP NUMBER, and its phone_number_id.
7. Finally, make sure to verify the number you intend to use for testing by
   entering it in the "To" field.
