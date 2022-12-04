# DBM Term Project
# UA-Technologies
# Andrew Santa and Danielle Harris

from sqlite3 import Binary
from flask import Flask
import csv
import psycopg2

# data[3] is headers
#data[496] is first real element
#data[][28] last column
def parse():
    with open("data.csv") as f:
        reader = csv.reader(f)
        data = list(reader)

    conn = psycopg2.connect("host=localhost dbname=events user=ads227 password=admin")
    cur = conn.cursor()

    # Populate event table
    for i in range(496, 818):
        # Process overhead
        tmp = data[i][11].strip(' $')
        tmp2 = tmp.strip('\'')
        data[i][11] = tmp2
        tmp = data[i][11].replace(',', '')
        data[i][11] = tmp
        if data[i][11] == '-':
            data[i][11] = 0

        # Process rentalFee
        tmp = data[i][6].strip(' $')
        tmp2 = tmp.strip('\'')
        data[i][6] = tmp2
        tmp = data[i][6].replace(',', '')
        data[i][6] = tmp
        if data[i][6] == '-':
            data[i][6] = 0

        # Remove meaningless values
        if data[i][1] != "#REF!" and data[i][4] != '':
            cur.execute("INSERT INTO event(title, category, hours, date, facilityname, facilityarea, overhead, rentalfee) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (data[i][0], data[i][3], data[i][4], data[i][5], data[i][1], data[i][2], data[i][11], data[i][6]))

    for i in range(1116, 1800):
        # Process overhead
        tmp = data[i][11].strip(' $')
        tmp2 = tmp.strip('\'')
        data[i][11] = tmp2
        tmp = data[i][11].replace(',', '')
        data[i][11] = tmp
        if data[i][11] == '-':
            data[i][11] = 0

        # Process rentalFee
        tmp = data[i][6].strip(' $')
        tmp2 = tmp.strip('\'')
        data[i][6] = tmp2
        tmp = data[i][6].replace(',', '')
        data[i][6] = tmp
        if data[i][6] == '-':
            data[i][6] = 0

        # Remove meaningless values
        if data[i][1] != "#REF!" and data[i][4] != '':
            cur.execute("INSERT INTO event(title, category, hours, date, facilityname, facilityarea, overhead, rentalfee) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (data[i][0], data[i][3], data[i][4], data[i][5], data[i][1], data[i][2], data[i][11], data[i][6]))

    # Populate department table
    cur.execute("INSERT INTO department(department) VALUES('PFOC'), ('AthleticsMaintenance'), ('AthleticsCustodial'), ('Ushers'), ('Trainers'), ('Parking'), ('Police'), ('Sound/Video'), ('Athletics')")

    conn.commit()


    # Populate eventStaffing
    for i in range(496, 818):
        try:
            print("i is %s PFOC", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'PFOC';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][13].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][13] = tmp2
            tmp = data[i][13].replace(',', '')
            data[i][13] = tmp
            if data[i][13] == '-':
                data[i][13] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][12], data[i][13]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s AthleticsMaintenance", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'AthleticsMaintenance';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][15].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][15] = tmp2
            tmp = data[i][15].replace(',', '')
            data[i][15] = tmp
            if data[i][15] == '-':
                data[i][15] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][14], data[i][15]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s AthleticsCustodial", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'AthleticsCustodial';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][17].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][17] = tmp2
            tmp = data[i][17].replace(',', '')
            data[i][17] = tmp
            if data[i][17] == '-':
                data[i][17] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][16], data[i][17]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s Ushers", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Ushers';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][19].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][19] = tmp2
            tmp = data[i][19].replace(',', '')
            data[i][19] = tmp
            if data[i][19] == '-':
                data[i][19] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][18], data[i][19]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s Trainers", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Trainers';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][21].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][21] = tmp2
            tmp = data[i][21].replace(',', '')
            data[i][21] = tmp
            if data[i][21] == '-':
                data[i][21] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][20], data[i][21]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s Parking", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Parking';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][23].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][23] = tmp2
            tmp = data[i][23].replace(',', '')
            data[i][23] = tmp
            if data[i][23] == '-':
                data[i][23] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][22], data[i][23]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s Police", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Police';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][25].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][25] = tmp2
            tmp = data[i][25].replace(',', '')
            data[i][25] = tmp
            if data[i][25] == '-':
                data[i][25] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][24], data[i][25]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s Sound/Video", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Sound/Video';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][27].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][27] = tmp2
            tmp = data[i][27].replace(',', '')
            data[i][27] = tmp
            if data[i][27] == '-':
                data[i][27] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][26], data[i][27]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

    for i in range(1116, 1800):
        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'PFOC';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][13].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][13] = tmp2
            tmp = data[i][13].replace(',', '')
            data[i][13] = tmp
            if data[i][13] == '-':
                data[i][13] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][12], data[i][13]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'AthleticsMaintenance';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][15].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][15] = tmp2
            tmp = data[i][15].replace(',', '')
            data[i][15] = tmp
            if data[i][15] == '-':
                data[i][15] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][14], data[i][15]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'AthleticsCustodial';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][17].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][17] = tmp2
            tmp = data[i][17].replace(',', '')
            data[i][17] = tmp
            if data[i][17] == '-':
                data[i][17] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][16], data[i][17]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Ushers';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][19].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][19] = tmp2
            tmp = data[i][19].replace(',', '')
            data[i][19] = tmp
            if data[i][19] == '-':
                data[i][19] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][18], data[i][19]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Trainers';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][21].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][21] = tmp2
            tmp = data[i][21].replace(',', '')
            data[i][21] = tmp
            if data[i][21] == '-':
                data[i][21] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][20], data[i][21]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Parking';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][23].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][23] = tmp2
            tmp = data[i][23].replace(',', '')
            data[i][23] = tmp
            if data[i][23] == '-':
                data[i][23] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][22], data[i][23]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Police';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][25].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][25] = tmp2
            tmp = data[i][25].replace(',', '')
            data[i][25] = tmp
            if data[i][25] == '-':
                data[i][25] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][24], data[i][25]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

        try:
            print("i is %s", str(i))
            if data[i][5] == '#REF!' or data[i][5] == '':
                continue
            cur.execute("select departmentid from department where department = 'Sound/Video';")
            departmentstring =  cur.fetchone()
            title = data[i][0]
            newTitle = title.replace("'", "''")
            print(newTitle)
            execString = "select eventid from event where date ='" + data[i][5] + "' and title = '" + newTitle + "';"
            cur.execute(execString)
            eventstring = cur.fetchone()
            # Process earnings
            tmp = data[i][27].strip(' $')
            tmp2 = tmp.strip('\'')
            data[i][27] = tmp2
            tmp = data[i][27].replace(',', '')
            data[i][27] = tmp
            if data[i][27] == '-':
                data[i][27] = 0
            cur.execute("INSERT INTO eventstaffing(departmentid, eventid, staff, earnings) VALUES(%s, %s, %s, %s)", (departmentstring, eventstring, data[i][26], data[i][27]))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        else:
            conn.commit()
            print(str(departmentstring) + str(eventstring))

parse()
