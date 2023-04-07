import pika
from pika.exchange_type import ExchangeType
import argparse


def main(args):
    connection_parameter = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameter)

    channel = connection.channel()
    channel.exchange_declare(exchange='headerexchange',
                             exchange_type=ExchangeType.headers)

    message = "Requesting Inference"

    # img_headers = {"type": "image",
    #             "url": "https://ultralytics.com/images/zidane.jpg",
    #             "output_location": "output"
    #             }
    # vid_headers = {"type": "video",
    #             "url": "https://cdn.pixabay.com/vimeo/724673230/lamb-120739.mp4?width=640&expiry=1680862434&hash=8b6cd86cf64d485c24fe1fc298eae5b93a99a900",
    #             "output_location": "output"
    #             }
    headers = {"type": args.type,
               "url": args.url,
               "output_location": args.output_path
               }

    channel.basic_publish(exchange='headerexchange',
                          routing_key='',
                          body=message,
                          properties=pika.BasicProperties(headers=headers))

    print(f'sent message: {message}')

    connection.close()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, help='image/video', default='image')
    parser.add_argument('--url', type=str, help='source of url', default='https://ultralytics.com/images/zidane.jpg')
    parser.add_argument('--output_path', type=str, help='location of output path', default='output')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
