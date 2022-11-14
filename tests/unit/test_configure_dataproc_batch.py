from dbt.adapters.bigquery.python_submissions import ServerlessDataProcHelper
from google.cloud import dataproc_v1

from .test_bigquery_adapter import BaseTestBigQueryAdapter

# Test application of dataproc_batch configuration to a
# google.cloud.dataproc_v1.Batch object.
# This reuses the machinery from BaseTestBigQueryAdapter to get hold of the
# parsed credentials
class TestConfigureDataprocBatch(BaseTestBigQueryAdapter):

    def test_configure_dataproc_serverless_batch(self):
        adapter = self.get_adapter('dataproc-serverless-configured')
        credentials = adapter.acquire_connection('dummy').credentials
        self.assertIsNotNone(credentials)

        batchConfig = credentials.dataproc_batch
        self.assertIsNotNone(batchConfig)

        raw_batch_config = self.raw_profile['outputs']['dataproc-serverless-configured']['dataproc_batch']
        raw_environment_config = raw_batch_config['environment_config']
        raw_execution_config = raw_environment_config['execution_config']
        raw_labels: dict[str, any] = raw_batch_config['labels']
        raw_rt_config = raw_batch_config['runtime_config']

        raw_batch_config = self.raw_profile['outputs']['dataproc-serverless-configured']['dataproc_batch']

        batch = dataproc_v1.Batch()

        ServerlessDataProcHelper._configure_batch_from_config(batchConfig, batch)

        # google's protobuf types expose maps as dict[str, str]
        to_str_values = lambda d: dict([(k, str(v)) for (k, v) in d.items()])

        self.assertEqual(batch.environment_config.execution_config.service_account, raw_execution_config['service_account'])
        self.assertFalse(batch.environment_config.execution_config.network_uri)
        self.assertEqual(batch.environment_config.execution_config.subnetwork_uri, raw_execution_config['subnetwork_uri'])
        self.assertEqual(batch.environment_config.execution_config.network_tags, raw_execution_config['network_tags'])
        self.assertEqual(batch.labels, to_str_values(raw_labels))
        self.assertEquals(batch.runtime_config.properties, to_str_values(raw_rt_config['properties']))


    def test_default_dataproc_serverless_batch(self):
        adapter = self.get_adapter('dataproc-serverless-default')
        credentials = adapter.acquire_connection('dummy').credentials
        self.assertIsNotNone(credentials)

        batchConfig = credentials.dataproc_batch
        self.assertIsNone(batchConfig)