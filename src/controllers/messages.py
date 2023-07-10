"""WhatsApp Messages Controller"""

import logging
import json

from heyoo import WhatsApp

from settings import Configurations

WHATSAPP_CREDENTIALS = json.loads(Configurations.WHATSAPP_CREDENTIALS)

logger = logging.getLogger(__name__)


def get_sender_creds(creds_list: list, sender: str) -> dict:
    """
    Get the credentials of the sender.

    :param creds_list: list - List of credentials.
    :param sender: str - Sender's phone number.

    :return: Sender's credentials if found, else None.
    :rtype: dict or None
    """
    try:
        logger.debug("Finding sender's credentials ...")

        for credential in creds_list:
            print(credential)
            if sender in credential.values():
                logger.info("Sender's credentials found")
                return credential
        return None

    except Exception as error:
        logger.error("Error getting sender's creds")
        raise error


def extract_metadata(data: dict) -> dict:
    """
    Extract metadata from the webhook data.

    :param data: dict - Webhook data.

    :return: Extracted metadata if found, else None.
    :rtype: dict or None
    """
    try:
        logger.debug("Extracting metadata ...")

        for entry in data["entry"]:
            for change in entry["changes"]:
                if "metadata" in change["value"]:
                    logger.info("Successfully extracted metadata")
                    return change["value"]["metadata"]
        return None

    except Exception as error:
        logger.error("Error extracting metadata")
        raise error


def send_text(sender: str, recipient: str, message: str) -> dict:
    """
    Send a text message.

    :param sender: str - Sender's phone number.
    :param recipient: str - Recipient's phone number.
    :param message: str - Message content.

    :return: Response from the messaging service.
    :rtype: dict or None
    """
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
        logger.error("Error sending text")
        raise error


def send_template(
    sender: str, template: str, recipient: str, components: list, lang: str
) -> dict:
    """
    Send a message using a template.

    :param sender: str - Sender's phone number.
    :param template: str - Template name.
    :param recipient: str - Recipient's phone number.
    :param components: list - List of message components.
    :param lang: str - Language code.

    :return: Response from the messaging service.
    :rtype: dict or None
    """
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
        logger.error("Error sending template")
        raise error


def receive_message(webhook_data: dict) -> dict:
    """
    Receive and process incoming messages from the webhook data.

    :param webhook_data: dict - Webhook data.

    :return: Processed message data.
    :rtype: dict or None
    """
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
                
        return None

    except Exception as error:
        logger.error("Error processing webhook")
        raise error
