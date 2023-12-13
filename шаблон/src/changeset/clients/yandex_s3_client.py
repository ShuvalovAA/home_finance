from typing import Dict, List, Tuple

import boto3

from changeset.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    BUCKET_NAME,
    ENDPOINT_URL,
    REGION_NAME,
    SERVICE_NAME,
)

__all__ = [
    'YandexS3'
]


class YandexS3:
    """Класс прокси клиента для взаимодействия с Yandex Object Storage."""

    def __init__(self, partner_id: int):
        self.partner_id = partner_id

    async def _get_client(self):
        """Получить клиент SDK для работы с YOS."""
        session = boto3.session.Session()
        client = session.client(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
            service_name=SERVICE_NAME,
            endpoint_url=ENDPOINT_URL
        )
        return client

    async def start_multipart_upload(self, key: str) -> Tuple[str, str]:
        """Инициализировать составную загрузку."""
        client = await self._get_client()
        result = client.create_multipart_upload(
            Bucket=BUCKET_NAME,
            Key=key
        )
        return result['Key'], result['UploadId']

    async def upload_part(self, file_path: str, key: str, multipart_id: str, part_number: str) -> str:
        """Загрузить фрагмент."""
        client = await self._get_client()
        with open(file_path, 'rb') as file:
            result = client.upload_part(
                Bucket=BUCKET_NAME,
                Key=key,
                UploadId=multipart_id,
                Body=file.read(),
                PartNumber=part_number
            )
        return result['ETag']

    async def abort_multipart_upload(
            self,
            key: str,
            multipart_id: str
    ) -> None:
        """Прерывать составную загрузку."""
        client = await self._get_client()
        client.abort_multipart_upload(
            Bucket=BUCKET_NAME,
            Key=key,
            UploadId=multipart_id,
        )

    async def complete_multipart_upload(self, key: str, multipart_id: str, parts_list: List[Dict[str, str]]):
        """Завершить составную загрузку."""
        client = await self._get_client()
        client.complete_multipart_upload(
            Bucket=BUCKET_NAME,
            Key=key,
            UploadId=multipart_id,
            MultipartUpload=parts_list
        )

    async def get_file_url(self, key: str) -> str:
        """Вернуть временную ссылку на объект для скачивания."""
        client = await self._get_client()
        file_url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=240,
            HttpMethod='GET'
        )
        return file_url
