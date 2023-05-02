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

image_url = 'https://static.todamateria.com.br/upload/58/4f/584f40614b3cd-taj-mahal.jpg'
domain = "landmarks"

# Analyze the image using the specified domain and model
analysis = cv_client.analyze_image_by_domain(model=domain, url=image_url)
for location in analysis.result.get(domain):
    print('Location name: {0}'.format(location['name']))
    print('Location confidence: {0:.2f}%'.format(location['confidence']*100))