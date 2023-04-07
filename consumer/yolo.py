import torch
import cv2
from ultralytics import YOLO
import os


class Detection:
    def __init__(self):
        self.model = YOLO('yolov5s.pt')
        self.model.info(False)

    def infer_image(self, url, outfile_name):
        # Images
        file_name = url.split('/')[-1]

        isExist = os.path.exists(outfile_name)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(outfile_name)

        try:
            torch.hub.download_url_to_file(url, file_name)
        except Exception as e:
            print(f"Couldn't downnlod Image. Error:{e}")
            return 0

        img = cv2.imread(file_name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Inference
        with torch.no_grad():
            results = self.model(img)

        # Save the output image
        img_out = results[0].plot()
        img_out = cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR)
        outfile_name = os.path.join(outfile_name, file_name)
        cv2.imwrite(outfile_name, img_out)
        return 1

    def infer_video(self, url, outfile_name):
        isExist = os.path.exists(outfile_name)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(outfile_name)

        file_name = url.split('/')[-1]
        outfile_name = os.path.join(outfile_name, file_name)
        try:
            torch.hub.download_url_to_file(url, file_name)
        except Exception as e:
            print(f"Couldn't downnlod Video. Error {e}")
            return 0

        stream = cv2.VideoCapture(url)
        fps = int(stream.get(cv2.CAP_PROP_FPS))
        frame_size = (
            int(stream.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            )
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(outfile_name, fourcc, fps, frame_size)

        while stream.isOpened():
            ret, frame = stream.read()

            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            with torch.no_grad():
                results = self.model(frame)

            annotated_frame = results[0].plot()
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
            writer.write(annotated_frame)

        stream.release()
        writer.release()
        return 1


if __name__ == '__main__':
    det = Detection()
    # url = 'https://ultralytics.com/images/zidane.jpg'  # batch of images
    # det.infer_image(url, 'output')

    url = 'https://cdn.pixabay.com/vimeo/724673230/lamb-120739.mp4?width=640&expiry=1680862434&hash=8b6cd86cf64d485c24fe1fc298eae5b93a99a900'
    det.infer_video(url, 'output')
