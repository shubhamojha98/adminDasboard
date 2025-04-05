from django.db import models, connection
from django.contrib.auth.hashers import check_password
from datetime  import datetime
from django.http import Http404

class AuthModel:
    
    def login(post_data,request):
        ins_array={
            "username":post_data['username'],
            "password":post_data['password'],
            "ipaddress":request.client_ip,
            'laitude':post_data['lat'],
            'longitude':post_data['long'],
            'entryby':0
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
        loginsert_query="""INSERT INTO tbl_login_logs (username,password, ipaddress, latitude, longitude,entryby)
            VALUES (%s, %s, %s, %s, %s,%s)"""
            
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
                        cursor.execute("UPDATE tbl_login_logs SET usertype= %s, loginid = %s, isloggedin= %s WHERE pk_id = %s",
                                                    ["default",user_rec['user_type_id'],"YES", log_id] )

                        if user_rec and post_data['username']== user_rec['user_name'] and post_data['password']== user_rec['password']  : 
                            print(user_rec) 
                            return user_rec
                        else:
                            raise Http404("Invalid username or password")
                    else:
                         raise Http404("User is not active")
            else:
                raise Http404("User not found")