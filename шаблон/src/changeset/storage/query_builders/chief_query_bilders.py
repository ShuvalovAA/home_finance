from datetime import date, datetime
from typing import Optional

__all__ = [
    'ChiefQueryBuilder'
]


class ChiefQueryBuilder:
    """Строитель запросов для руководителя загрузки."""

    def __init__(self, partner_id: int):
        self.partner_id = partner_id

    class PGQueries:
        """Запросы для PostgreSQL."""

        INSERT = '''
            INSERT INTO uploading_parts(
                process_id,
                status,
                start_date,
                part_position
            )
            VALUES(
                {process_id},
                {status},
                '{start_date}',
                {part_position}
            ) RETURNING id;
        '''

        UPDATE = '''
            UPDATE uploading_parts
            SET
                status={status},
                part_position={part_position},
                etag='{etag}'
            WHERE 1=1
                AND process_id={process_id}
                AND id={id}
        '''

        GET_ALL_PARTS_LIST_CREDS = '''
            SELECT
                etag, part_position
            FROM
                uploading_parts
            WHERE
                process_id={process_id}
        '''

        UPDATE_UPLOAD_RECORD = '''
            UPDATE multipart_upload
            SET
                status={status},
                parts_count={parts_count}
                {msg_abort}
            WHERE 1=1
                AND partner_id={partner_id}
                AND id={id}
        '''

        GET_STORAGE_KEY_AND_MULTIPART_UPLOAD = '''
            SELECT
                storage_key,
                multipart_id
            FROM
                multipart_upload
            WHERE
                id = {id}
        '''

    class CHQueries:
        """Запросы для ClickHouse."""

        SELECT = '''
            SELECT
                table, toString(operation_date) as operation_date, after_data, before_data, operation_type
            FROM test_logs
            WHERE 1=1
                    AND partner_id = {partner_id}
                    AND table='{table_name}'
                    AND operation_date BETWEEN '{period_start}' and '{period_end}'
            ORDER BY  id OFFSET {offset} ROW FETCH FIRST {limit} ROWS ONLY
        '''

    def _clean_q_for_ch(self, query: str) -> str:
        query_str = ' '.join(w.strip() for w in query.split() if w).replace(
            '\n', ''
        )
        return query_str

    def build_query_pg_get_query_insert_pg(
            self,
            process_id: int,
            status: int,
            part_position: int
    ) -> str:
        """Построить запрос на создании записи о фрагменте."""
        query = self.PGQueries.INSERT.format(
            process_id=process_id,
            status=status,
            start_date=datetime.now(),
            part_position=part_position
        )
        return query

    def build_query_pg_get_query_update_part_record(
            self,
            process_id: int,
            part_id: int,
            status: int,
            part_position: int,
            etag: str
    ) -> str:
        """Построить запрос на обновление записи о фрагменте."""
        query = self.PGQueries.UPDATE.format(
            process_id=process_id,
            id=part_id,
            status=status,
            part_position=part_position,
            etag=etag
        )
        return query

    def build_query_pg_get_query_update_upload_record(
            self,
            process_id: int,
            status: int,
            parts_count: int,
            msg_abort: Optional[str] = None
    ) -> str:
        """Построить запрос обновления записи."""
        query = self.PGQueries.UPDATE_UPLOAD_RECORD.format(
            id=process_id,
            partner_id=self.partner_id,
            status=status,
            parts_count=parts_count,
            msg_abort=f",msg_abort='{msg_abort}'" if msg_abort else ''
        )
        return query

    def build_query_ch_get_query_select_ch(
            self,
            limit: int,
            offset: int,
            target_table: str,
            period_start: date,
            period_end: date,
    ) -> str:
        """Построить запрос на получение данных по фрагменту."""
        query = self.CHQueries.SELECT.format(
            table_name=target_table,
            partner_id=self.partner_id,
            period_start=period_start,
            period_end=period_end,
            offset=offset,
            limit=limit
        )
        return self._clean_q_for_ch(query)

    def build_query_get_all_parts_list(self, process_id: int):
        """Построить запрос га возврат списка словарей всех фрагментов с ETag и PartNumber."""
        query = self.PGQueries.GET_ALL_PARTS_LIST_CREDS.format(
            process_id=process_id
        )
        return self._clean_q_for_ch(query)

    def build_query_get_upload_key_and_multipart_id(self, process_id: int) -> str:
        """Построить запрос возврата ключа и id составной загрузки."""
        query = self.PGQueries.GET_STORAGE_KEY_AND_MULTIPART_UPLOAD.format(
            id=process_id
        )
        return query
