import json
import random
import base64

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

IMAGE_WIDTH = 800
IMAGE_HEIGHT = 480

MARGIN_LEFT = 80
MARGIN_RIGHT = 80

def handler(event, context):
    f = open("quotes.json", "r")
    quotes = json.loads(f.read())
    quote = random.choice(quotes)

    out = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0))

    # https://fonts.google.com/specimen/Inria+Serif?query=inria
    font = ImageFont.truetype("Inria_Serif/InriaSerif-LightItalic.ttf", 20)
    d = ImageDraw.Draw(out)

    text = '"' + quote["body"] + '"'
    author = quote["author"]

    if quote["originName"]:
        author = author + ", " + quote["originName"]

    lines = []

    # https://itnext.io/how-to-wrap-text-on-image-using-python-8f569860f89e
    if font.getsize(text)[0] > IMAGE_WIDTH:
        words = text.split(' ')
        i = 0

        while i < len(words):
            line = ''

            while i < len(words) and font.getsize(line + words[i])[0] <= IMAGE_WIDTH - (MARGIN_LEFT + MARGIN_RIGHT):
                line = line + words[i]+ " "
                i += 1

            if not line:
                line = words[i]
                i += 1

            lines.append(line)

    else:
        lines.append(text)

    lines.append("")
    lines.append(author)

    text = "\n".join(lines)

    text_w, text_h = font.getsize_multiline(text)
    top = (IMAGE_HEIGHT / 2) - (text_h / 2)
    left = (IMAGE_WIDTH / 2) - (text_w / 2)

    d.multiline_text(
        (left, top),
        text,
        font=font,
        fill=(255, 255, 255),
        align="center"
    )

    # https://stackoverflow.com/a/33117447/1561941
    output = BytesIO()
    out.save(output, format='JPEG')
    im_data = output.getvalue()

    # https://forums.aws.amazon.com/thread.jspa?threadID=268584
    data = base64.b64encode(im_data).decode('ascii')

    # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-payload-encodings-workflow.html
    # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-payload-encodings-configure-with-control-service-api.html
    # https://medium.com/@adil/how-to-send-an-image-as-a-response-via-aws-lambda-and-api-gateway-3820f3d4b6c8
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/jpeg"
        },
        "body": data,
        "isBase64Encoded": True
    }

# res = handler({}, {})
# print(res)

