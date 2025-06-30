from PIL import Image
import imagehash

def calc_hash_similarity(uploaded_hash, template_image, hash_size=128) -> float:
    template_hash = imagehash.average_hash(template_image, hash_size=hash_size)
    diff = uploaded_hash - template_hash
    return 1 - (diff / (hash_size**2))
