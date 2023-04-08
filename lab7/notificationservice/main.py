import base64
import json
import logging
import os
import functions_framework

from pub_sub_util import create_topic, publish_message


@functions_framework.cloud_event
def receive_order_status(cloud_event):
    data = cloud_event.data
    event_id = cloud_event["id"]
    logging.basicConfig(level=logging.INFO)
    logging.info("""This Function was triggered by EventId {}""".format(event_id))
    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    data = json.loads(base64.b64decode(data).decode('utf-8'))
    custom_event_type = cloud_event['attributes'].get("event_type")
    logging.info("""The application specific event type is {}""".format(custom_event_type))
    create_topic(project=project_id, topic="order_status_user")
    if custom_event_type == "OrderCreated":
        order_id = data["id"]
        data = {
            "message": "The order was accepted. The order id is {}.".format(order_id)
        }
        data = json.dumps(data).encode("utf-8")
        publish_message(project=project_id, topic="order_status_user", message=data, event_type="OrderAccepted")
    else:
        data = {
            "message": "Sorry, we can not meet your order at the moment. Please try later."
        }
        data = json.dumps(data).encode("utf-8")
        publish_message(project=project_id, topic="order_status_user", message=data, event_type="OrderRejected")
