import zipfile

def is_suspected_zip_bomb(zip_path, ratio_threshold=10, max_uncompressed=500_000_000):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        total_uncompressed = sum(i.file_size for i in zf.infolist())
        total_compressed = sum(i.compress_size for i in zf.infolist())
        ratio = total_uncompressed / max(total_compressed, 1)

        if ratio > ratio_threshold or total_uncompressed > max_uncompressed:
            return True
    return False

print(is_suspected_zip_bomb("test_bomb.zip"))