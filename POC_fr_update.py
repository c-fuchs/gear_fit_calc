#POC to update fit_reports table with user_ and gear_ bust and waist

def fr_update(fr_id):
    
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
        
        #get fr_gear_id from fit reports
        sql1 = ("SELECT fr_gear_id FROM fit_reports WHERE fr_id = %s")
        val1 = (fr_id,) #casting fr_id as tuple, so %s works
        cursor.execute(sql1,val1)
        res1 = cursor.fetchone()
        fr_gear_id = int(res1[0]) #casting cursor result as int, since cursor returns a tuple(s)
        print(fr_gear_id)
        #get fr_user_id from fit reports
        sql1a = ("SELECT fr_user_id FROM fit_reports WHERE fr_id = %s")
        cursor.execute(sql1a,val1)
        res1a = cursor.fetchone()
        fr_user_id = int(res1a[0]) #casting cursor result as int, since cursor returns a tuple
        print(fr_user_id)
        
        #get gear_derived_bust value from gear and store as gear_bust
        sql2 = ("SELECT gear_derived_bust FROM gear WHERE gear_id = %s")
        val2 = (fr_gear_id,)
        cursor.execute(sql2,val2)
        res2 = cursor.fetchone()
        gear_bust = float(res2[0])
        print(gear_bust)
        #get gear_derived_waist value from gear and store as gear_waist
        sql2a = ("SELECT gear_derived_waist FROM gear WHERE gear_id = %s")
        cursor.execute(sql2a,val2)
        res2a = cursor.fetchone()
        gear_waist = float(res2a[0])
        print(gear_waist)

        #get user_bust value from users and store as user_bust
        sql3 = ("SELECT user_bust FROM users WHERE user_id = %s")
        val3 = (fr_user_id,)
        cursor.execute(sql3,val3)
        res4 = cursor.fetchone()
        user_bust = float(res4[0])
        print(user_bust)
        #get user_waist value from users and store as user_waist
        sql3a = ("SELECT user_waist FROM users WHERE user_id = %s")
        cursor.execute(sql3a,val3)
        res4a = cursor.fetchone()
        user_waist = float(res4a[0])
        print(user_waist)

        #get fr_bust_adjust value from fit_reports
        sql3b = ("SELECT fr_bust_adjust FROM fit_reports WHERE fr_id = %s")
        cursor.execute(sql3b,val1)
        res5 = cursor.fetchone()
        fr_bust_adjust = float(res5[0])
        print(fr_bust_adjust)
        #get fr_waist_adjust value from fit_reports
        sql3c = ("SELECT fr_waist_adjust FROM fit_reports WHERE fr_id = %s")
        cursor.execute(sql3c,val1)
        res5a = cursor.fetchone()
        fr_waist_adjust = float(res5a[0])
        print(fr_waist_adjust)

        #get back_pro from fit_reports
        sql4 = ("SELECT fr_backpro FROM fit_reports WHERE fr_id = %s")
        cursor.execute(sql4,val1)
        res6 = cursor.fetchone()
        fr_backpro = int(res6[0])
        print(fr_backpro)

        #calculate gear_bust_est for this fit report
        gear_bust_est = (gear_bust + user_bust + fr_bust_adjust + fr_backpro)/2
        print(gear_bust_est)
        #calculate gear_waist_est for this fit report
        gear_waist_est = (gear_waist + user_waist + fr_waist_adjust + (fr_backpro/2))/2
        print(gear_waist_est)
        #calculate user_bust_est for this fit report
        user_bust_est = (gear_bust_est + user_bust + fr_bust_adjust)/2
        print(user_bust_est)
        #calculate user_waist_est for this fit report
        user_waist_est = (gear_waist_est + user_waist + fr_waist_adjust)/2
        print(user_waist_est)
    
        #update gear_bust_est in fit_reports table 
        sql5 = ("UPDATE fit_reports SET gear_bust_est = %s WHERE fr_id = %s")
        val4 = gear_bust_est, fr_id
        cursor.execute(sql5,val4)
        mydb.commit()
        print("db updated with gear_bust_est of " + str(gear_bust_est))
        #update gear_waist_est in fit_reports table 
        sql5 = ("UPDATE fit_reports SET gear_waist_est = %s WHERE fr_id = %s")
        val4a = gear_waist_est, fr_id
        cursor.execute(sql5,val4a)
        mydb.commit()
        print("db updated with gear_waist_est of " + str(gear_waist_est))
        #update user_bust_est in fit_reports table
        sql6 = ("UPDATE fit_reports SET user_bust_est = %s WHERE fr_id = %s")
        val5 = user_bust_est, fr_id
        cursor.execute(sql6,val5)
        mydb.commit()
        print("db updated with user_bust_est of " + str(user_bust_est))
        #update user_waist_est in fit_reports table
        sql6a = ("UPDATE fit_reports SET user_waist_est = %s WHERE fr_id = %s")
        val5a = user_waist_est, fr_id
        cursor.execute(sql6a,val5a)
        mydb.commit()
        print("db updated with user_waist_est of " + str(user_waist_est))
 
    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if (mydb.is_connected()):
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")    
 
for x in range(1,17):
    fr_update(x)
    x+=1
