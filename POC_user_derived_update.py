#updates derived measurements for a single user_id with multiple fit report values

def user_derived_update(user_id):
    
    #sql connector goes here
    import mysql.connector
    from mysql.connector import Error
    
    try: 
        mydb = mysql.connector.connect(
        host = 'localhost',
        port = ####,
        user = '####',
        password = '####',
        auth_plugin='mysql_native_password',
        database = "gear_fit_calc",
        )
        
        print("MySQL connection open")

        cursor = mydb.cursor() 

        bust_records = []

        #create the sql query to get all bust vals from from fit_reports, and save records as tuple
        sql1 = ("SELECT user_bust_est FROM fit_reports WHERE fr_user_id = %s")
        val1 = (user_id,)
        cursor.execute(sql1,val1)
        res1 = cursor.fetchall()
        print(str(res1))
        for row in res1:
            bust_records.append(row[0])
        print(bust_records)
        bust = float(sum(bust_records)/len(bust_records))
        print(bust)

        waist_records = []
        #create the sql query to get all waist vals from from fit_reports, and save records as tuple
        sql1 = ("SELECT user_waist_est FROM fit_reports WHERE fr_user_id = %s")
        val1 = (user_id,)
        cursor.execute(sql1,val1)
        res1 = cursor.fetchall()
        print(str(res1))
        for row in res1:
            waist_records.append(row[0])
        print(waist_records)
        waist = float(sum(waist_records)/len(waist_records))
        print(waist)

        #update user_derived_bust with new value
        sql2 = ("UPDATE users SET user_derived_bust = %s WHERE user_id = %s")
        val2 = bust, user_id
        cursor.execute(sql2,val2)
        mydb.commit()
        print("db updated with user_derived_bust of " + str(bust))

        #update user_derived_waist with new value
        sql2 = ("UPDATE users SET user_derived_waist = %s WHERE user_id = %s")
        val2 = waist, user_id
        cursor.execute(sql2,val2)
        mydb.commit()
        print("db updated with user_derived_waist of " + str(waist))

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if (mydb.is_connected()):
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")   

for x in range(1,9):
    user_derived_update(x)
    x+=1
