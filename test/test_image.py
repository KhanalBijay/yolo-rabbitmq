import os
import pika
from pika.exchange_type import ExchangeType
import pytest
import time


@pytest.fixture
def image_fixture():
    url = "https://ultralytics.com/images/zidane.jpg"
    output = "output"
    type = "image"

    connection_parameter = pika.ConnectionParameters("localhost")
    connection = pika.BlockingConnection(connection_parameter)

    channel = connection.channel()
    channel.exchange_declare(
        exchange="headerexchange", exchange_type=ExchangeType.headers
    )

    message = "Requesting Inference"

    headers = {"type": type, "url": url, "output_location": output}

    channel.basic_publish(
        exchange="headerexchange",
        routing_key="",
        body=message,
        properties=pika.BasicProperties(headers=headers),
    )

    # Release the image object
    connection.close()


def test_image_file_name(image_fixture):
    # Verify that the presence of output file with filename
    time.sleep(5)
    assert os.path.exists("output/zidane.jpg")
