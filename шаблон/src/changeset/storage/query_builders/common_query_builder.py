__all__ = [
    'CommonQueryBuilder'
]


class CommonQueryBuilder:
    """Строитель запроса для общих методово взаимодействия с хранилищем."""

    def __init__(self, partner_id):
        self.partner_id = partner_id

    class PGQueries:
        """Запросы для PostgreSQL."""

        GET_UPLOADING_STATUS = '''
            SELECT
                status
            FROM
                multipart_upload
            WHERE 1=1
                AND id={process_id}
                AND partner_id={partner_id}
        '''

    def build_query_get_uploading_status(
            self,
            process_id: int,
    ) -> str:
        """Построить запрос получения статуса составной загрузки."""
        query = self.PGQueries.GET_UPLOADING_STATUS.format(
            partner_id=self.partner_id,
            process_id=process_id
        )
        return query
