from datetime import date, datetime

__all__ = [
    'StarterQueryBuilder'
]


class StarterQueryBuilder:
    """Строитель запросов для стартера загрузки."""

    def __init__(self, partner_id: int):
        self.partner_id = partner_id

    class PGQueries:
        """Запросы для PostgreSQL."""

        INSERT = '''
            INSERT INTO multipart_upload(
                partner_id,
                status,
                target_table,
                start_date,
                period_start,
                period_end,
                parts_count,
                storage_key,
                multipart_id
            )
            VALUES(
                {partner_id},
                {status},
                '{target_table}',
                '{start_date}',
                '{period_start}',
                '{period_end}',
                {parts_count},
                '{storage_key}',
                '{multipart_id}'
            ) RETURNING id;
        '''

    def build_query_pg_get_query_insert(
            self,
            status: int,
            target_table: str,
            period_start: date,
            period_end: date,
            storage_key: str,
            multipart_id: str
    ) -> str:
        """Построить запрос добавления записи."""
        query = self.PGQueries.INSERT.format(
            partner_id=self.partner_id,
            status=status,
            target_table=target_table,
            period_start=period_start,
            period_end=period_end,
            parts_count=0,
            start_date=datetime.now(),
            storage_key=storage_key,
            multipart_id=multipart_id
        )
        return query
