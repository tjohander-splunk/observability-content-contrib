import json
import requests
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.metrics import (
    get_meter_provider,
    set_meter_provider,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

exporter = OTLPMetricExporter(endpoint='localhost:4317', headers=None, insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
set_meter_provider(provider)
meter = get_meter_provider().get_meter("lambda-demo")
counter = meter.create_counter("lambda-demo-counter")


def lambda_handler(event, context):
    x = requests.get('https://w3schools.com/python/demopage.htm')
    print(x.text)

    counter.add(1, attributes={
        "attribute-key": "my-counter-attribute",
        "another-attribute-key": "another-attribute-value"
    })

    return {
        'statusCode': 200,
        'body': json.dumps(x.text)
    }
