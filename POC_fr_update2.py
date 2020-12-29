#POC to update fit_reports table with user_ and gear_ bust and waist

def fr_update():
    
    #sql connector goes here
    import mysql.connector
    from mysql.connector import Error
    
    try: 
        mydb = mysql.connector.connect(
        host = 'localhost',
        port = 2083,
        user = '####',
        password = '####',
        auth_plugin='mysql_native_password',
        database = "gear_fit_calc",
        )
        print("MySQL connection open")

        cursor = mydb.cursor() 
    
        #get values from form submission JSON
        user_bust = hello.event.queryStringParameters.bust
        user_waist = hello.event.queryStringParameters.waist
        gear_brand = hello.event.queryStringParameters.gear_brand
        gear_name = hello.event.queryStringParameters.gear_name
        gear_size = hello.event.queryStringParameters.size
        fr_bust_adjust = hello.event.queryStringParameters.bust_adjust
        fr_waist_adjust = hello.event.queryStringParameters.waist_adjust
        fr_backpro = hello.event.queryStringParameters.backpro

        #get fr_gear_id from gear
        sql1 = ("SELECT gear_id FROM gear WHERE gear_brand = %s AND gear_name = %s AND gear_size = %s")
        val1 = (gear_brand, gear_name, gear_size) #casting as tuples, so %s works
        cursor.execute(sql1,val1)
        res1 = cursor.fetchone()
        fr_gear_id = int(res1[0]) #casting cursor result as int, since cursor returns a tuple(s)
        print(fr_gear_id)
        #get fr_user_id from fit reports
        sql2 = ("SELECT fr_user_id FROM fit_reports WHERE fr_id = %s")
        cursor.execute(sql1a,val1)
        res2 = cursor.fetchone()
        fr_user_id = int(res2[0]) #casting cursor result as int, since cursor returns a tuple
        print(fr_user_id)
        
        #get gear_derived_bust value from gear and store as gear_bust
        sql3 = ("SELECT gear_derived_bust FROM gear WHERE gear_id = %s")
        val3 = (fr_gear_id,)
        cursor.execute(sql3,val3)
        res3 = cursor.fetchone()
        gear_bust = float(res3[0])
        print(gear_bust)
        #get gear_derived_waist value from gear and store as gear_waist
        sql4 = ("SELECT gear_derived_waist FROM gear WHERE gear_id = %s")
        val4 = val3
        cursor.execute(sql4,val4)
        res4 = cursor.fetchone()
        gear_waist = float(res4[0])
        print(gear_waist)

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
        val5 = gear_bust_est, fr_id
        cursor.execute(sql5,val5)
        mydb.commit()
        print("db updated with gear_bust_est of " + str(gear_bust_est))
        #update gear_waist_est in fit_reports table 
        sql6 = ("UPDATE fit_reports SET gear_waist_est = %s WHERE fr_id = %s")
        val6 = gear_waist_est, fr_id
        cursor.execute(sql6,val6)
        mydb.commit()
        print("db updated with gear_waist_est of " + str(gear_waist_est))
        #update user_bust_est in fit_reports table
        sql7 = ("UPDATE fit_reports SET user_bust_est = %s WHERE fr_id = %s")
        val7 = user_bust_est, fr_id
        cursor.execute(sql7,val7)
        mydb.commit()
        print("db updated with user_bust_est of " + str(user_bust_est))
        #update user_waist_est in fit_reports table
        sql8 = ("UPDATE fit_reports SET user_waist_est = %s WHERE fr_id = %s")
        val8 = user_waist_est, fr_id
        cursor.execute(sql8,val58)
        mydb.commit()
        print("db updated with user_waist_est of " + str(user_waist_est))
 
    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if (mydb.is_connected()):
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")    
