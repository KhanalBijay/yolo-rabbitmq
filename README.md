# yolo-rabbitmq

### Install python packages
` pip install -r requirements.txt `

### To run rabbitmq on docker
` docker-compose build `
` docker-compose up `

### To run consumer
` python3 consumer/app.py `

### To request to infer video/image
` python3 producer/client.py --type <image/video> --output <location of output> --url <url>`
