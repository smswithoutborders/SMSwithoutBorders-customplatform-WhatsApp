# API V1 References

This documentation provides an overview of the API version 1 endpoints and their
usage.

## Table of Contents

1. [Messages](#messages)
   - [Send Message](#send-message)
   - [Receive Message (webhook)](#receive-message)

---

## Messages

Resources for managing messages.

### Send Message

Sends a message of the specified type.

**Endpoint**

```
POST v1/send/:message_type
```

**Headers**

| Attribute      | Value            | Required | Description                                                                                                              |
| :------------- | :--------------- | :------- | :----------------------------------------------------------------------------------------------------------------------- |
| `Content-Type` | application/json | Yes      | Used to indicate the original [media type](https://developer.mozilla.org/en-US/docs/Glossary/MIME_type) of the resource. |

**Parameters**

| Parameter      | Type   | Required | Description                                                                       |
| :------------- | :----- | :------- | :-------------------------------------------------------------------------------- |
| `message_type` | string | Yes      | Specifies the type of the message to send. Possible values: "text" or "template". |

**Body**

The request body should be in JSON format and contain the following attributes:

| Attribute    | Type   | Required                              | Description                             |
| :----------- | :----- | :------------------------------------ | :-------------------------------------- |
| `sender`     | string | Yes                                   | The sender of the message.              |
| `recipient`  | string | Yes                                   | The recipient of the message.           |
| `message`    | string | Yes (for `message_type` = "text")     | The text message to send.               |
| `template`   | string | Yes (for `message_type` = "template") | The template to use for the message.    |
| `components` | array  | Yes (for `message_type` = "template") | The components of the template message. |
| `lang`       | string | Yes (for `message_type` = "template") | The language of the template message.   |

**Example Request**

```shell
curl --location 'https://staging.smswithoutborders.com:18000/v1/send/:message_type' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sender": "+123456789",
    "recipient": "+123456789",
    "message": "",
    "template": "hello_world",
	"components": [{
		"type": "body",
		"parameters": [
			{
				"type": "text",
				"text": "your-text-string"
			},
			{
				"type": "currency",
				"currency": {
					"fallback_value": "$100.99",
					"code": "USD",
					"amount_1000": 100990
				}
			},
			{
				"type": "date_time",
				"date_time" : {
					"fallback_value": "February 25, 1977",
					"day_of_week": 5,
					"day_of_month": 25,
					"year": 1977,
					"month": 2,
					"hour": 15,
					"minute": 33
				}
			},
			{
			"type": "date_time",
				"date_time" : {
				"fallback_value": "February 25, 1977",
				"timestamp": 1485470276
				}
			}
		]
	}],
    "lang": "en_US"
}'
```

**Example Responses**

> [200] Successful

- This response indicates that the request was completed successfully.

```json
{
	"contacts": [
		{
			"input": "+123456789",
			"wa_id": "123456789"
		}
	],
	"messages": [
		{
			"id": "wamid.------"
		}
	],
	"messaging_product": "whatsapp"
}
```

> [400] Bad Request

- This response is returned when some attributes are missing from the request
  data.

> [404] Not Found

- This response is returned when the sender is not found.

> [500] Internal Server Error

- This response is returned when an unexpected error occurs.

### Receive Message

Receive webhook data.

**Endpoint**

```
POST/GET v1/receive
```

**GET Request**

When making a GET request to this endpoint, it is used for webhook verification.
The request should include the following parameters:

**Parameters**

| Parameter          | Type   | Required | Description                                                                      |
| :----------------- | :----- | :------- | :------------------------------------------------------------------------------- |
| `hub.verify_token` | string | Yes      | A verification token used to verify the webhook.                                 |
| `hub.challenge`    | string | Yes      | A challenge string provided by the Facebook Messenger platform for verification. |

If the verification token matches the expected value of the
`WHATSAPP_VERIFY_TOKEN` environment variable, the endpoint returns a successful
response with an HTTP status code of `200`. The response body contains the
challenge string.

**POST Request**

When making a POST request to this endpoint, it is used to process webhook data.
The request body should be in JSON format and contain the following attributes:

**Body**

| Attribute      | Type | Required | Description                                            |
| :------------- | :--- | :------- | :----------------------------------------------------- |
| `webhook_data` | JSON | Yes      | The webhook data received from the messenger platform. |

If the recipient is found and the webhook data is processed successfully, the
newly received message payload is sent to all the URLs in the `WEBHOOK_URLS`
environment variable.

```json
{
	"recipient_phone_number": "",
	"sender_name": "",
	"sender_phone_number": "",
	"message": "",
	"message_id": ""
}
```

**Example Responses**

> [200] Successful

- This response indicates that the request was completed successfully.

```text/plain
OK
```

> [400] Bad Request

- This response is returned when some attributes are missing from the request
  data.

> [404] Not Found

- This response is returned when the sender is not found.

> [500] Internal Server Error

- This response is returned when an unexpected error occurs.
