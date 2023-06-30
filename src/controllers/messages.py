"""WhatsApp Messages Controller"""

import logging
import json

from heyoo import WhatsApp

from settings import Configurations

WHATSAPP_CREDENTIALS = json.loads(Configurations.WHATSAPP_CREDENTIALS)

logger = logging.getLogger(__name__)


def get_sender_creds(creds_list, sender):
    """"""
    logger.debug("Finding sender's credentials ...")

    for credential in creds_list:
        print(credential)
        if sender in credential.values():
            logger.info("Sender's credentials found")
            return credential
    return None


def extract_metadata(data):
    """"""

    logger.debug("Extracting metadata ...")

    for entry in data["entry"]:
        for change in entry["changes"]:
            if "metadata" in change["value"]:
                logger.info("Successfully extracted metadata")
                return change["value"]["metadata"]
    return None


def send_text(sender, recipient, message):
    """"""
    try:
        sender_creds = get_sender_creds(creds_list=WHATSAPP_CREDENTIALS, sender=sender)

        if not sender_creds:
            logger.error("Sender '%s' Not Found", sender)
            return None

        messenger = WhatsApp(
            sender_creds["access_token"],
            phone_number_id=sender_creds["phone_number_id"],
        )
        response = messenger.send_message(message, recipient)

        return response

    except Exception as error:
        raise error


def send_template(sender, template, recipient, components, lang):
    """"""
    try:
        sender_creds = get_sender_creds(creds_list=WHATSAPP_CREDENTIALS, sender=sender)

        if not sender_creds:
            logger.error("Sender '%s' Not Found", sender)
            return None

        messenger = WhatsApp(
            sender_creds["access_token"],
            phone_number_id=sender_creds["phone_number_id"],
        )
        response = messenger.send_template(
            template=template, recipient_id=recipient, components=components, lang=lang
        )

        return response

    except Exception as error:
        raise error


def receive_message(webhook_data):
    """"""
    try:
        metadata = extract_metadata(data=webhook_data)

        if not metadata:
            logger.error("No webhook metadata")
            return None

        business = metadata["phone_number_id"]
        business_creds = get_sender_creds(
            creds_list=WHATSAPP_CREDENTIALS, sender=business
        )

        if not business_creds:
            logger.error("Business '%s' Not Found", business)
            return None

        messenger = WhatsApp(
            business_creds["access_token"],
            phone_number_id=business_creds["phone_number_id"],
        )

        logging.debug("Received webhook data: %s", webhook_data)

        changed_field = messenger.changed_field(webhook_data)
        if changed_field == "messages":
            new_message = messenger.get_mobile(webhook_data)
            if new_message:
                sender_mobile = messenger.get_mobile(webhook_data)
                sender_name = messenger.get_name(webhook_data)
                message_type = messenger.get_message_type(webhook_data)
                message = messenger.get_message(webhook_data)
                message_id = messenger.get_message_id(webhook_data)

                logging.debug(
                    "New Message; sender_mobile:%s sender_name:%s message_type:%s, message: %s, message_id: %s",
                    sender_mobile,
                    sender_name,
                    message_type,
                    message,
                    message_id,
                )

                if message_type == "text":
                    return {
                        **business_creds,
                        "sender_name": sender_name,
                        "sender_mobile": sender_mobile,
                        "message": message,
                        "message_id": message_id,
                    }

    except Exception as error:
        raise error
