import os
import io
import json
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests
from PIL import Image, ImageDraw, ImageFont


# API credentials
credentials = json.load(open('credentials.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']
cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))


image_url = 'https://scoutdoor.com.br/blog/wp-content/uploads/2020/02/18.jpg'
downloaded_image = requests.get(image_url)


request = cv_client.read(image_url, raw=True)
operationLocation = request.headers['Operation-Location']
operationId = operationLocation.split('/')[-1]


response = cv_client.get_read_result(operationId)
while response.status != OperationStatusCodes.succeeded:
    response = cv_client.get_read_result(operationId)


if response.status == OperationStatusCodes.succeeded:
    analysis = response.analyze_result.read_results
    for analyzed_results in analysis:
        for line in analyzed_results.lines:
            print(line.text)


image = Image.open(io.BytesIO(downloaded_image.content))
if response.status == OperationStatusCodes.succeeded:
    analysis = response.analyze_result.read_results
    for analyzed_results in analysis:
        for line in analyzed_results.lines:
            for word in line.words:
                x1, y1, x2, y2, x3, y3, x4, y4 = word.bounding_box
                draw = ImageDraw.Draw(image)
                draw.line(
                    ((x1, y1), (x2, y1), (x2, y2), (x3, y2), (x3, y3), (x4, y3), (x4, y4), (x1, y4), (x1, y1)),
                    fill=(255, 0, 0),
                    width=5
                )


if os.path.exists("hand writing result.jpg"):
    os.remove("hand writing result.jpg")

image.show()
image.save("hand writing result.jpg")

