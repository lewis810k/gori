import os

from django.core.files.uploadedfile import SimpleUploadedFile


def image_upload():
    file_path=os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'talent'),'test_image.jpg')
    test_image = SimpleUploadedFile(name='test_image.jpg', content=open(file_path, 'rb').read(),
                                    content_type='image / jpeg')
    return test_image



