import datetime

from airflow import models
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

from custom_ops import CustomTransformationOperator

# If you are running Airflow in more than one time zone
# see https://airflow.apache.org/docs/apache-airflow/stable/timezone.html
# for best practices
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    'owner': 'Composer Example',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': YESTERDAY,
}

with models.DAG(
        'composer_quickstart',
        catchup=False,
        default_args=default_args,
        schedule_interval=datetime.timedelta(days=1)) as dag:

    download = GCSToLocalFilesystemOperator(
        task_id="download_data",
        object_name="sales.csv",
        bucket="adadata",
        filename="/tmp/sales.csv"
    )

    transform = CustomTransformationOperator(
        task_id='transform_data', file_name='/tmp/sales.csv')

    upload = LocalFilesystemToGCSOperator(
        task_id='upload_data',
        bucket='adadata',
        src="{{ task_instance.xcom_pull(task_ids='transform_data') }}",
        # See https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html for Xcoms
        dst='sales_sum.csv'
    )

    download >> transform >> upload  # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html#control-flow
