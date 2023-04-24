import cv2
import PyPDF2
from PIL import Image
import numpy as np
import io


def extractFaces(image, scaleFactor=1.4, exibir=False):
    faces = []
    try:
        # Carregar a imagem
        image = cv2.imdecode(np.frombuffer(
            image, np.uint8), cv2.IMREAD_UNCHANGED)

        # Carregar o classificador de rostos
        face_cascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")

        # Converter a imagem para escala de cinza
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detectar rostos na imagem
        faces = face_cascade.detectMultiScale(
            gray_image, scaleFactor=scaleFactor, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0 and exibir:
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Mostrar a imagem com os rostos detectados
            cv2.imshow("Rostos detectados", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    except:
        pass
    return len(faces) > 0


def extractImages(pdf):
    if isinstance(pdf, bytes):
        pdf = io.BytesIO(pdf)
        pdf_reader = PyPDF2.PdfReader(pdf)
    elif isinstance(pdf, str):
        pdf_file = open(pdf, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
    else:
        raise ValueError("Os tipos permitidos sao somente bytes[] ou string")

    images = []

    for page in pdf_reader.pages:
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()

            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj]._data
                    mode = ''
                    if '/ColorSpace' in xObject[obj] and xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = 'RGB'
                    else:
                        mode = 'P'
                    images.append(data)
    return images


def isFaceDetected(pdf):
    images = extractImages(pdf)
    for image in images:
        if extractFaces(image):
            return True
    return False