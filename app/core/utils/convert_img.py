import base64


def convert_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_str = base64.b64encode(f.read())
    return "data:image/png;base64," + image_str.decode('utf-8')