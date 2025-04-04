from django.db import models, connection
from django.contrib.auth.hashers import check_password

class AuthModel:
    @staticmethod
    def login(post_data,request):
        ins_array={
            "user_name":post_data['username'],
            "password":post_data['password'],
            "ipaddress":request.client_ip,
            'laitude':post_data['lat'],
            'longitude':post_data['long'],
            'login_datetime':datetime.now()
        }
        #or create tuple liek this
        # log_values = [
        #     post_data['username'],
        #     post_data['password'],  # Use hashed password in production
        #     request.client_ip,
        #     post_data['latitude'],
        #     post_data['longitude'],
        #     datetime.now()
        # ]
        loginsert_query="""INSERT INTO tbl_user_logs (user_name, password, ipaddress, latitude, longitude, login_datetime)
            VALUES (%s, %s, %s, %s, %s, %s)"""
            
        with connection.cursor() as cursor:
            cursor.execute(loginsert_query ,tuple(ins_array.values()))
            # cursor.execute(loginsert_query ,log_values)
            
            cursor.execute("Select LAST_INSERT_ID()")
            log_id = cursor.fetchone()[0]
               
            cursor.execute("SELECT * FROM tbl_user_master WHERE user_name = %s", [post_data['username']])
            row = cursor.fetchone()
            if row: 
                    columns = [col[0] for col in cursor.description]
                    user_rec=dict(zip(columns, row))
                    if user_rec['is_active']:
                        cursor.execute("UPDATE tbl_user_logs SET user_type = %s WHERE pk_id = %s",
                                                    [user_rec['user_type_id'], log_id] )

                        if user_rec and post_data['username']== user_rec['user_name'] and post_data['password']== user_rec['password']  :  
                            return user_rec
        return None