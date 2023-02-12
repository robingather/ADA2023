from publisher import create_topic
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    create_topic("ada2023", "diabetes_req")
    create_topic("ada2023", "diabetes_res")
