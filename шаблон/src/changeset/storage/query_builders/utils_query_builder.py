import datetime

__all__ = [
    'UtilsQueryBuilder'
]


class UtilsQueryBuilder:
    """Строитель запросов для утилит."""

    class PGQueries:
        """Запросы для PostgreSQL."""

        CHECK_LAST_PARTNER_UPLOAD_PROCESS = '''
            SELECT
            EXISTS(
                select *
                from
                    multipart_upload
                where 1=1
                    AND partner_id={partner_id}
                    AND start_date > NOW() - interval '{time} minute'
            );
        '''

    class CHQueries:
        """Запросы для ClickHouse."""

        CHECK_DATA_EXISTS = '''
            SELECT exists(
                SELECT *
                FROM test_logs
                WHERE partner_id={partner_id}
                    AND operation_date BETWEEN '{period_start}' AND '{period_end}'
            )
        '''

    def build_query_check_last_partner_upload_process(self, time_throttling: int) -> str:
        """Построить запрос проверки процесса, запущенного в последнее время."""
        query = self.PGQueries.CHECK_LAST_PARTNER_UPLOAD_PROCESS.format(
            partner_id=self.partner_id,
            time=time_throttling
        )
        return query

    def build_query_check_data_exists(
            self,
            target_table: str,
            period_start: datetime.date,
            period_end: datetime.date
    ) -> str:
        """Построить запрос проверки процесса, запущенного в последнее время."""
        query = self.CHQueries.CHECK_DATA_EXISTS.format(
            partner_id=self.partner_id,
            target_table=target_table,
            period_start=period_start,
            period_end=period_end
        )
        return query
