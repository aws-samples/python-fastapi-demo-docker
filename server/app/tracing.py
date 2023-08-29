"""
This file contains all the required libraries to implement Open Telemetry with Fast API
"""

import os
# Add imports for OTel components into the application
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.metrics import CallbackOptions, Observation
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

# Import the AWS X-Ray for OTel Python IDs Generator into the application.
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator

# To Get Resource Detector for AWS EKS
from opentelemetry.sdk.resources import get_aggregated_resources
from opentelemetry.sdk.extension.aws.resource.eks import (
    AwsEksResourceDetector,
)

# Instrumentation Package for SQL Alechemy
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


# Sends generated traces in the OTLP format to an ADOT Collector running on port 4317
otlp_exporter = OTLPSpanExporter(endpoint=f"http://{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}")
# Processes traces in batches as opposed to immediately one after the other
span_processor = BatchSpanProcessor(otlp_exporter)
# Configures the Global Tracer Provider
trace.set_tracer_provider(
    TracerProvider(
         resource=get_aggregated_resources(
            [
                AwsEksResourceDetector(),
            ]
        ), active_span_processor=span_processor, id_generator=AwsXRayIdGenerator()))

# Fast API Instrumentor Library
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

