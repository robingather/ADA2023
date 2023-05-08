import logging

from user_consumer import create_subscription
from user_publisher import create_topic

logging.getLogger().setLevel(logging.INFO)
create_topic("ada23-project", "order_req") # make sure to change the project id
create_subscription("ada23-project", "order_req", "order_req_sub")
create_topic("ada23-project", "inventory_status")
create_topic("ada23-project", "order_status")
create_topic("ada23-project", "order_status_user")
create_subscription("ada23-project", "order_status_user", "order_status_user_sub")
create_topic("ada23-project", "order_req")
create_topic("ada23-project", "inventory_status")
create_subscription("ada23-project", "inventory_status",
                    "inventory_status_sub")
create_subscription("ada23-project", "order_status","order_status_sub")
