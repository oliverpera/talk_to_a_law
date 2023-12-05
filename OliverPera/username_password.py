import psycopg2

def check_password_correct(username, password):
    conn = psycopg2.connect(database="postgres", user="postgres", password="OLI123oli", host="localhost", port="5432")

    cur = conn.cursor()
    sql = """ SELECT * FROM mqtt.username_password WHERE mqtt.username_password.username = 'admin' """
    cur.execute(sql)
    rows = cur.fetchall()
    
    values_listed = separate_tuple_values(rows)
        
    if (values_listed[0][0], values_listed[1][0]) == (username, password):
        return True
    else:
        return False
    

def separate_tuple_values(tuple_list):
    separated_lists = [[] for _ in range(len(tuple_list[0]))]

    for tpl in tuple_list:
        for i, value in enumerate(tpl):
            separated_lists[i].append(value)
            
    return separated_lists

if __name__ == "__main__":
    print(check_password_correct('admin', 'admin'))  