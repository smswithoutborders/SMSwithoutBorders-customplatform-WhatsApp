"""Version 1 API endpoints"""

import logging

from flask import Blueprint, request

from werkzeug.exceptions import BadRequest

from src.controllers.messages import send_text, send_template, receive_message

v1 = Blueprint(name="v1", import_name=__name__, url_prefix="/v1")

logger = logging.getLogger(__name__)


@v1.route(rule="/send/<string:message_type>", methods=["POST"])
def send_message(message_type):
    try:
        data = request.get_json()

        if not data.get("sender"):
            logger.error("No Sender Provided")
            raise BadRequest()

        if not data.get("recipient"):
            logger.error("No Recipient Provided")
            raise BadRequest()

        if message_type == "text":
            if not data.get("message"):
                logger.error("No Message Provided")
                raise BadRequest()

            sender = data.get("sender")
            recipient = data.get("recipient")
            message = data.get("message")

            res = send_text(sender=sender, recipient=recipient, message=message)

        elif message_type == "template":
            if not data.get("template"):
                logger.error("No Template Provided")
                raise BadRequest()

            if not isinstance(data.get("components"), list):
                logger.error("Components must be list")
                raise BadRequest()

            if not data.get("lang"):
                logger.error("No Lang Provided")
                raise BadRequest()

            sender = data.get("sender")
            recipient = data.get("recipient")
            template = data.get("template")
            components = data.get("components")
            lang = data.get("lang")

            res = send_template(
                sender=sender,
                recipient=recipient,
                components=components,
                template=template,
                lang=lang,
            )

        return res, 200

    except BadRequest as error:
        return str(error), 400

    except Exception as error:
        logger.exception(error)
        return "Internal Server Error", 500


@v1.route(rule="/receive", methods=["POST"])
def receive_web_hook():
    try:
        data = request.get_json()

        res = receive_message(webhook_data=data)

        print("\n", res)

        return "", 200

    except BadRequest as error:
        return str(error), 400

    except Exception as error:
        logger.exception(error)
        return "Internal Server Error", 500
