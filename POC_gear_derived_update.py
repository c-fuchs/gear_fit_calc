#POC update for gear_derived_bust
#updates derived measurements for a single gear_id with multiple fit report values

def gear_derived_update(gear_id):
    
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
        #create the sql query to get bust records from fit_reports, and save records as list
        sql1 = ("SELECT gear_bust_est FROM fit_reports WHERE fr_gear_id = %s")
        val1 = (gear_id,)
        cursor.execute(sql1,val1)
        res1 = cursor.fetchall()
        for row in res1:
            bust_records.append(row[0])
        print(bust_records)
        #need to add a pass condition here so we don't divide by zero
            #if bust_records has 0 items 
        bust = float(sum(bust_records)/len(bust_records))
        print(bust)

        waist_records = []
        #create the sql query to get waist records from fit_reports, and save records as list
        sql1a = ("SELECT gear_waist_est FROM fit_reports WHERE fr_gear_id = %s")
        cursor.execute(sql1a,val1)
        res1 = cursor.fetchall()
        for row in res1:
            waist_records.append(row[0])
        print(waist_records)
        #need to add a pass condition here so we don't divide by zero
            #if bust_records has 0 items 
        waist = float(sum(waist_records)/len(waist_records))
        print(waist)

        #update gear_derived_bust with new value
        sql2 = ("UPDATE gear SET gear_derived_bust = %s WHERE gear_id = %s")
        val2 = bust, gear_id
        cursor.execute(sql2,val2)
        mydb.commit()
        print("db updated with gear_derived_bust of " + str(bust))

        #update gear_derived_waist with new value
        sql2a = ("UPDATE gear SET gear_derived_waist = %s WHERE gear_id = %s")
        val2a = waist, gear_id
        cursor.execute(sql2a,val2a)
        mydb.commit()
        print("db updated with gear_derived_waist of " + str(waist))

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if (mydb.is_connected()):
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")   

for x in range(2,12):
    gear_derived_update(x)
    x+=1
