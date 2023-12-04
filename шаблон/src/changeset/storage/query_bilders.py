"""Строители запросов."""
from datetime import datetime, date
from typing import Optional


class UploadingDirectorQueryBuilder:
    """Строитель запросов для процесса многосоставной загрузки."""
    def __init__(self, partner_id):
        self.partner_id = partner_id
    class PGQueries:
        INSERT = """
        INSERT INTO 
            multipart_upload(
                partner_id,
                status,
                target_table,
                start_date,
                period_start,
                period_end,
                parts_count,
                file_url
            )
        VALUES(
            {partner_id},
            {status},
            '{target_table}',
            '{start_date}',
            '{period_start}',
            '{period_end}',
            {parts_count},
            {file_url}
        );
        SELECT currval('multipart_upload_id_seq') as id;
        """

        UPDATE = """
        UPDATE multipart_upload
        SET 
            status={status},
            parts_count={parts_count},
            file_url={file_url}
        WHERE 1=1
            AND partner_id={partner_id}
            AND id={id}
        """

    def build_query_pg_get_query_insert(
            self,
            partner_id: int,
            status: int,
            target_table: str,
            period_start: date,
            period_end: date,
    ) -> str:
        """Построить запрос добавления записи."""
        query = self.PGQueries.INSERT.format(
            partner_id=self.partner_id,
            status=status,
            target_table=target_table,
            period_start=period_start,
            period_end=period_end,
            parts_count=0,
            file_url='null',
            start_date=datetime.now()
        )
        return query

    def build_query_pg_get_query_update(
            self,
            process_id: int,
            status: int,
            parts_count: int,
            file_url: Optional[str] = None
    ) -> str:
        """Построить запрос обновления записи."""
        query = self.PGQueries.UPDATE.format(
            id=process_id,
            partner_id=self.partner_id,
            status=status,
            parts_count=parts_count,
            file_url=file_url or 'null'
        )
        return query


class UploaderQueryBuilder:
    """Строитель запросов для фрагмента процесса многосоставной загрузки."""
    def __init__(self, partner_id):
        self.partner_id = partner_id

    class PGQueries:
        INSERT = """
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
        );
        SELECT currval('uploading_parts_id_seq') as id;
        """

        UPDATE = """
        UPDATE uploading_parts
        SET 
            status={status},
            part_position={part_position}
        WHERE 1=1
            AND process_id={process_id}
            AND id={id}
        """

    class CHQueries:
        SELECT = """
        SELECT 
            table, ts_ms, after_data, before_data, op
        FROM test_logs
        WHERE 1=1
                AND partner_id = {partner_id}
                AND table='{table_name}'
                AND ts_ms BETWEEN '{period_start}' and '{period_end}'
        ORDER BY  id OFFSET {offset} ROW FETCH FIRST {limit} ROWS ONLY
        """

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

    def build_query_pg_get_query_update_pg(
            self,
            process_id: int,
            part_id: int,
            status: int
        ) -> str:
        """Построить запрос на обновление записи о фрагменте."""
        query = self.PGQueries.UPDATE.format(
            process_id=process_id,
            id=part_id,
            status=status,
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


class UtilsQueryBuilder:
    """Строитель запросов для утилит."""
    class PGQueries:
        CHECK_LAST_PARTNER_UPLOAD_PROCESS = """
        SELECT 
        EXISTS(
            select * 
            from 
                multipart_upload 
            where 1=1
                AND partner_id={partner_id}
                AND start_date < NOW() - interval '{time} minute'
        );
        """

    def build_query_check_last_partner_upload_process(self, time_throttling: int) -> str:
        """Построить запрос проверки процесса, запущенного в последнее время."""
        query = self.PGQueries.CHECK_LAST_PARTNER_UPLOAD_PROCESS.format(
            partner_id=self.partner_id,
            time=time_throttling
        )
        return query

