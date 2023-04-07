import pika
from pika.exchange_type import ExchangeType
import argparse


def main(args):
    connection_parameter = pika.ConnectionParameters("localhost")
    connection = pika.BlockingConnection(connection_parameter)

    channel = connection.channel()
    channel.exchange_declare(
        exchange="headerexchange", exchange_type=ExchangeType.headers
    )

    message = "Requesting Inference"
    headers = {
        "type": args.type,
        "url": args.url,
        "output_location": args.output_path,
    }  # noqa E501

    channel.basic_publish(
        exchange="headerexchange",
        routing_key="",
        body=message,
        properties=pika.BasicProperties(headers=headers),
    )

    print(f"sent message: {message}")

    connection.close()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, help="image/video")
    parser.add_argument("--url", type=str, help="source of url")
    parser.add_argument(
        "--output_path",
        type=str,
        help="location of output path",
        default="output",  # noqa E501
    )
    opt = parser.parse_args()

    return opt


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
