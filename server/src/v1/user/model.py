from db import Db
import hashlib

class UserModel():
    def sanitize(self, users):
        if not isinstance(users, (list, tuple)):
            users = [users]
        clean_users = []
        for user in users:
            if not isinstance(user, dict):
                continue
            if not ('id' in user and 'username' in user and 'password' in user):
                continue
            clean_users.append(user)
        return clean_users

    def create(self, users):
        if not isinstance(users, (list, tuple)):
            users = [users]
        clean_users = self.sanitize(users)
        if len(users) != len(clean_users):
            return False
        queries = []
        #users['username'],users['password'] = self.encrypt(users['username'],users['password'])
        for user in clean_users:
            sql = "INSERT INTO users(username,password) VALUES(%s,%s)"
            queries.append({"sql": sql, "bind": (user['username'],user['password'])})
        db = Db.get_instance()
        result = db.transactional(queries)
        return users

    def read(self, filters=None, count_only=False):
        db = Db.get_instance()
        fields = ['*']
        offset = 0
        limit = 5
        if filters is not None:
            if 'fields' in filters:
                tmp_fields = []
                for field in filters['fields']:
                    if field in ['id', 'username', 'password']:
                        tmp_fields.append(field)
                if len(tmp_fields) > 0:
                    fields = tmp_fields
            if 'id' in filters:
                sql = "SELECT " + ','.join(fields) + " FROM users WHERE id = %s"
                user = db.fetchone(sql, filters['id'])
                return user
            if 'offset' in filters:
                offset = int(filters['offset'])
            if 'limit' in filters:
                limit = int(filters['limit'])
        cols = 'COUNT(*) AS total' if count_only else ','.join(fields)
        sql = "SELECT " + cols + " FROM users"
        if not count_only:
            sql += " ORDER BY username LIMIT " + str(offset) + ", " + str(limit)
        if count_only:
            row = db.fetchone(sql)
            return row['total'] if row else 0
        else:
            return db.fetchall(sql)

    def update(self, users):
        if not isinstance(users, (list, tuple)):
            users = [users]
        clean_users = self.sanitize(users)
        if len(users) != len(clean_users):
            return False
        queries = []
        for user in clean_users:
            sql = "UPDATE users SET username = %s, password = %s WHERE id = %s"
            queries.append({"sql": sql, "bind": (user['username'], user['password'], user['id'])})
        db = Db.get_instance()
        db.transactional(queries)
        return users

    def delete(self, users):
        counter = 0
        if not isinstance(users, (list, tuple)):
            users = [users]
        placeholder = []
        queries = []
        for user in users:
            placeholder.append('%s')
        sql = "DELETE FROM users WHERE id IN (" + ", ".join(placeholder) + ")"
        queries.append({"sql": sql, "bind": users})
        db = Db.get_instance()
        counter = db.transactional(queries)
        return counter
    
    @staticmethod
    def exists(username, password):
        #username,password = self.encrypt(username,password)
        sql = "SELECT CASE WHEN EXISTS(SELECT 1 from users WHERE username=%s and password=%s) then 1 ELSE 0 END AS exist;"
        db = Db.get_instance()
        return db.fetchone(sql, (username,password))

    @staticmethod
    def encrypt(self,user,password):
        user = hashlib.sha256(user.encode()) 
        password = hashlib.sha256(password.encode()) 
        # printing the equivalent hexadecimal value.
        #print("The hexadecimal equivalent of SHA256 is : ")
        #print(result.hexdigest())
        return user.hexdigest(),password.hexdigest()
