import pika
from pika.exchange_type import ExchangeType
from yolo import Detection

det = Detection()


def on_video_received(ch, method, properties, body):
    url = properties.headers['url']
    output_location = properties.headers['output_location']
    print(f'Received video: {url}, {output_location}')
    ret = det.infer_video(url, output_location)
    if ret:
        print("Completed Video inference")
    else:
        print("Couldn't complete process")


def on_image_received(ch, method, properties, body):
    url = properties.headers['url']
    output_location = properties.headers['output_location']
    print(f'Received Image: {url}, {output_location}')
    ret = det.infer_image(url, output_location)
    if ret:
        print("Completed Image inference")
    else:
        print("Couldn't complete process")


connection_parameter = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameter)

channel = connection.channel()
channel.exchange_declare(exchange='headerexchange',
                         exchange_type=ExchangeType.headers)

queue_vid = channel.queue_declare(queue='video_queue')
queue_img = channel.queue_declare(queue='image_queue')

channel.queue_bind(queue='video_queue', exchange='headerexchange',
                   arguments={'x-match': 'all', 'type': 'video'})
channel.basic_consume(queue='video_queue', auto_ack=True,
                      on_message_callback=on_video_received)

channel.queue_bind(queue='image_queue', exchange='headerexchange',
                   arguments={'x-match': 'all', 'type': 'image'})
channel.basic_consume(queue='image_queue', auto_ack=True,
                      on_message_callback=on_image_received)

print("Start consuming")
channel.start_consuming()
