#Rank gear by best fit and return records to user
#deal with jackets only for now, add suits, pants later

def gear_fetcher(user_id):
    #connector stuff goes here
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

        #LATER: add a filter so that we don't have to search the whole database. 
        #Add user linear inches (eg bust+waist+hips > 34+24+34= 92 )
        #Return only records within 6 linear inches of user's linear inches

        #get user derived bust from users
        sql1 = ("SELECT user_derived_bust FROM users WHERE user_id = %s")
        val1 = (user_id,)
        cursor.execute(sql1,val1)
        res1 = cursor.fetchone()
        user_derived_bust = res1[0]
        print(user_derived_bust)
        #get user derived waist from users
        sql1a = ("SELECT user_derived_waist FROM users WHERE user_id = %s")
        cursor.execute(sql1a,val1)
        res1a = cursor.fetchone()
        user_derived_waist = res1a[0]
        print(user_derived_waist)

        #select all records from gear and compare bust measurements to user
        sql2 = ("SELECT * FROM gear")
        cursor.execute(sql2)
        records = cursor.fetchall()
        gear_id, gear_brand, gear_name, gear_size, gear_derived_bust, gear_derived_waist, bust_variance, waist_variance, total_variance = [],[],[],[],[],[],[],[],[]
        for row in records:
            gear_id.append(row[0])
            gear_brand.append(row[1])
            gear_name.append(row[2])
            gear_size.append(row[3])
            gear_derived_bust.append(row[4])
            gear_derived_waist.append(row[5])
            variance_b = (row[4] - user_derived_bust)**2 #squared to make it positive
            bust_variance.append(variance_b) 
            variance_w = (row[5] - user_derived_waist)**2 #squared to make it positive
            waist_variance.append(variance_w)
            variance_tot = variance_b + variance_w
            total_variance.append(variance_tot)

        #find the index of the gear with the least variance from the user
        bf_index = total_variance.index(min(total_variance))

        #print results for user, limit to top 10
        print("Here are your 10 best jacket fit results: \n")
        for i in range (0,10):
            print(str(gear_brand[bf_index]) + ' ' + str(gear_name[bf_index]) + ' in size ' + str(gear_size[bf_index]) + ' has a variance of ' + str(total_variance[bf_index]**0.5) + ' inches. ')
            gear_brand.remove(gear_brand[bf_index])
            gear_name.remove(gear_name[bf_index])
            gear_size.remove(gear_size[bf_index])
            bust_variance.remove(bust_variance[bf_index])
            waist_variance.remove(waist_variance[bf_index])
            total_variance.remove(total_variance[bf_index])
            bf_index = total_variance.index(min(total_variance))
            i += 1 

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if (mydb.is_connected()):
            cursor.close()
            mydb.close()
            print("MySQL connection is closed")   

gear_fetcher(2)
