import utils

if __name__ == '__main__':
    images = utils.extractImages("rg_exemplo.pdf")
    for image in images:
        utils.extractFaces(image, exibir=True)
