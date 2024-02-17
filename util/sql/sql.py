import sqlite3
import os


class Sql:
    __conn = None
    __curr = None
    __db_path = ""
    __db_name = "db.db"

    def install(self):
        
        conn = sqlite3.connect(self.__db_path)
        curr = conn.cursor()
        with open("db.sql", encoding="utf8") as f:
            for s in f.read().split(";"):
                print(s)
                curr.execute(s)
                conn.commit()

        curr.close()
        conn.close()
        print("数据库安装成功")

    def connect(self, path):
        self.__db_path = os.path.join(path, self.__db_name)
        self.__conn = sqlite3.connect(self.__db_path)
        self.__curr = self.__conn.cursor()
        return self

    def close_curr(self):
        self.__curr.close()
        return self

    def connect_curr(self):
        self.__curr = self.__conn.cursor()
        return self

    def close(self):
        self.__curr.close()
        self.__conn.close()
        return self

    def insert_image(self, md5_name, src, path, name, suffix, authority, img_type):
        
        self.__curr.execute(
            "insert into photo (md_name, path, src, name, suffix, authority, type) values "
            "(?, ?, ?, ?, ?, ?, ?)",
            [md5_name, path, src, name, suffix, authority, img_type]
        )
        self.__conn.commit()
        return True

    def select_photo_md_name(self, md_name):
        
        result = self.__curr.execute(
            "select * from photo where md_name = ?", [md_name]
        )
        return result.fetchone()

    def select_photo_md_name_auth(self, md_name, authority):
        
        result = self.__curr.execute(
            "select * from photo where md_name = ? and authority = ?",
            [md_name, authority]
        )
        return result.fetchone()

    def select_photo_range(self, limit=0, offset=20):
        
        return self.__curr.execute(
            "select * from photo order by id desc limit ? offset ?", [limit, offset]
        ).fetchall()

    def select_type_photo_range(self, t, limit=0, offset=20):
        
        return self.__curr.execute(
            "select * from photo where type = ? order by id desc limit ? offset ?",
            [t, limit, offset]
        ).fetchall()

    def select_authority_photo_range(self, auth, limit=0, offset=20):
        
        return self.__curr.execute(
            "select * from photo where authority = ? order by id desc limit ? offset ?",
            [auth, limit, offset]
        ).fetchall()

    def get_photo_length(self):
        
        return self.__curr.execute(
            "select count(*) from photo"
        ).fetchone()[0]

    def get_type_length(self, t):
        
        return self.__curr.execute(
            "select count(*) from photo where type = ?", [t]
        ).fetchall()

    def get_authority_type_length(self, auth):
        
        return self.__curr.execute(
            "select count(*) from photo where authority = ?", [auth]
        ).fetchall()

    def select_types(self):
        
        return self.__curr.execute(
            "select type from photo group by type"
        ).fetchall()

    def select_type_photo(self, t):
        
        return self.__curr.execute(
            "select * from photo where type = ? and authority != 'admin' and authority != 'user' "
            "order by random() limit 1", [t]
        ).fetchone()

    def select_authority_photo(self, auth):
        
        return self.__curr.execute(
            "select * from photo where authority = ? order by random() limit 1",
            [auth]
        ).fetchone()

    def select_access_code_all(self):
        
        return self.__curr.execute("select * from access_code").fetchall()

    def insert_access_code(self, user, code):
        
        self.__curr.execute(
            "insert into access_code (user, code) values (?, ?)",
            [user, code]
        )
        self.__conn.commit()
        return True

    def delete_access_code(self, code):
        
        result = self.__curr.execute(
            "delete from access_code where code = ?",
            [code]
        )
        self.__conn.commit()

        if result.rowcount > 0:
            return True
        else:
            return False

    def select_access_code(self, code):
        
        return self.__curr.execute(
            "select * from access_code where code = ?",
            [code]
        ).fetchone()

    def delete_photo(self, md):
        
        result = self.__curr.execute(
            "delete from photo where md_name = ?", [md]
        )
        self.__conn.commit()
        if result.rowcount > 0:
            return True
        else:
            return False


if __name__ == '__main__':
    sql = Sql().connect(".")
    sql.install()
