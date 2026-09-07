import uuid
from src.utils.storage_service import s3_client
from src.security.config import settings


def upload_product_image_to_cloud(file, product_id):
    extension = file.filename.split(".")[-1]

    filename = f"products/{product_id}/{uuid.uuid4()}.{extension}"

    s3_client.upload_fileobj(
        file.file,
        settings.AWS_BUCKET_NAME,
        filename,
        ExtraArgs={"ContentType": file.content_type},
    )

    image_url = (
        f"https://{settings.AWS_BUCKET_NAME}.s3."
        f"{settings.AWS_REGION}.amazonaws.com/{filename}"
    )

    return image_url
