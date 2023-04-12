from imcslms.settings import PRIVATE_MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
from hashlib import sha1

def gen_hash_name(data: str) -> str:
    return sha1(data.encode()).hexdigest()

private_storage = FileSystemStorage(location=PRIVATE_MEDIA_ROOT)