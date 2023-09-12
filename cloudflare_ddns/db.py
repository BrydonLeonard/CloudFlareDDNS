import sqlite3, time

class DB:
    def __init__(self, db_path):
        if (db_path is None):
            self.db_path = "./dns.db"
        else:
            self.db_path = db_path

        # If the DB path is bad, this will throw
        self._configure_db()
        
        
    def get_latest_cached_ip(self):
        """
        Retrieves the latest cached IP for this machine or `None` if no IP is cached.
        """
        return self._query_and_return_first(
            """
                select v4address from ip 
                order by first_seen desc
                limit 1
            """,
            None
        )

    def get_record_id(self, domain_name):
        """
        Retrieves the CloudFlare record ID for the given domain name or `None` if the record 
        is not present in the DB
        """
        return self._query_and_return_first(
            """
                select record_id from record
                where domain_name = ?
                limit 1
            """,
            [domain_name]
        )

    def get_zone_id(self, domain_name):
        """
        Retrieves the CloudFlare record ID for the given domain name or `None` if the record 
        is not present in the DB
        """
        return self._query_and_return_first(
            """
                select zone_id from record
                where domain_name = ?
                limit 1
            """,
            [domain_name]
        )
        
    def cache_ip(self, ip):
        statement = """
            insert into ip(v4address, first_seen)
            values (?,?)
        """

        con = self._get_db_connection()
        con.execute(statement, (ip, round(time.time())))
        con.commit()
        con.close()

    def cache_record(self, record_id, domain_name, zone_id):
        existing_record = self._query_and_return_first("""
            select domain_name from record where domain_name = ?
        """, [domain_name])

        if (existing_record is None):
            statement = """
                insert into record(record_id, domain_name, zone_id)
                values (?, ?, ?)
            """
        else:
            statement = """
                update record set 
                    record_id=?, 
                    domain_name=?, 
                    zone_id=?
            """

        con = self._get_db_connection()
        con.execute(statement, [record_id, domain_name, zone_id])
        con.commit()
        con.close()

    # Private #
        
    def _query_and_return_first(self, query, params):
        """
        Executes the given query (using the params tuple to populate prepared statements if provided) 
        and returns the first element of the first row in the result
        """
        con = self._get_db_connection()
        cursor = con.cursor()
        if (params != None):
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()
        con.close()

        if len(results) == 0:
            return None
        else:
            return results[0][0]


    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _configure_db(self):
        con = self._get_db_connection()
        con.executescript("""
            create table if not exists ip(
                v4address text primary key,
                first_seen long not null
            );
                          
            create table if not exists record(
                record_id text primary key,
                domain_name text not null,
                zone_id text not null
            );
            """)
        con.close()