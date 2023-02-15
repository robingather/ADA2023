import json
import logging
import os

import functions_framework
import google.cloud.aiplatform as aip


def run_pipeline_job(name, pipeline_def, pipeline_root, parameter_dict):
    # Opening JSON file
    f = open(parameter_dict)
    data = json.load(f)
    print(data)
    logging.info(data)
    job = aip.PipelineJob(
        display_name=name,
        enable_caching=False,
        template_path=pipeline_def,
        pipeline_root=pipeline_root,
        parameter_values=data)
    job.run()


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def build_diabetes_predictor(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket_name}")
    print(f"File: {file_name}")

    name = os.environ.get('PIPELINE_NAME', 'Specified environment variable is not set.')
    pipeline_def = os.environ.get('PIPELINE_FILE', 'Specified environment variable is not set.')
    pipeline_root = os.environ.get('PIPELINE_ROOT_BUCKET', 'Specified environment variable is not set.')
    parameter_dict = os.environ.get('PARAMETERS_FILE', 'Specified environment variable is not set.')

    print('PIPELINE_NAME: {}'.format(name))
    print('PIPELINE_FILE: {}'.format(pipeline_def))
    print('PIPELINE_ROOT_BUCKET: {}'.format(pipeline_root))
    print('PARAMETERS_FILE: {}'.format(parameter_dict))

    run_pipeline_job(name=name, pipeline_def=pipeline_def, pipeline_root=pipeline_root, parameter_dict=parameter_dict)
    logging.info("Vertex AI Pipeline was submitted")
