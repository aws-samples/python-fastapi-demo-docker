import os
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from server.app.models import Base, Book
from server.app.connect import db_session, engine

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




app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

Base.metadata.create_all(bind=engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
)


def get_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/create_book")
def create_book_form(request: Request):
    return templates.TemplateResponse("create_book.html", {"request": request})


@app.post("/books")
def create_book_api(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
):
    book = Book(title=title, author=author, description=description)
    db.add(book)
    db.commit()
    db.refresh(book)
    return RedirectResponse(url="/books", status_code=303)


@app.get("/books")
def list_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse(
        "list_books.html", {"request": request, "books": books}
    )


@app.get("/books/{book_id}")
def read_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    return templates.TemplateResponse(
        "book_details.html", {"request": request, "book": book}
    )


@app.get("/books/{book_id}/update")
def update_book_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    return templates.TemplateResponse(
        "update_book.html", {"request": request, "book": book}
    )


@app.post("/books/{book_id}/update")
def update_book(
    request: Request,
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
):
    book = get_book(db, book_id)
    book.title = title
    book.author = author
    book.description = description
    db.commit()
    return RedirectResponse(url=f"/books/{book_id}", status_code=303)


@app.delete("/books/{book_id}")
def delete_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = get_book(book_id, db)
    db.delete(book)
    db.commit()
    return templates.TemplateResponse(
        "delete_book.html", {"request": request, "book": book}
    )
