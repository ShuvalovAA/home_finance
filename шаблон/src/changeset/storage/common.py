from changeset.exceptions import PartnerOrUploadNotFound
from changeset.storage.connectors import Connectors
from changeset.storage.query_builders.common_query_builder import CommonQueryBuilder

__all__ = [
    'StorageCommon'
]


class StorageCommon:
    """Хранилище общих методов."""

    def __init__(self, connectors: Connectors):
        self.partner_id = connectors.partner_id
        self.query_builder = CommonQueryBuilder(partner_id=self.partner_id)
        self.pg_connector = connectors.pg_connector

    async def get_uploading_status(self, uploading_id: int):
        """Вернуть статус процесса составной загрузки."""
        query = self.query_builder.build_query_get_uploading_status(process_id=uploading_id)
        async with self.pg_connector() as client:
            await client.execute(query)
            result = await client.fetchone()
        if not result:
            raise PartnerOrUploadNotFound
        return result[0]
