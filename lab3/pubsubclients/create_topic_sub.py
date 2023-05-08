from publisher import create_topic
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    create_topic("ada23-project", "diabetes_req")   # replace ada2023 with your project id
    create_topic("ada23-project", "diabetes_res") # replace ada2023 with your project id
