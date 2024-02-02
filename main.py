import psycopg2

def create_db(conn):
   with conn as x:
       with x.cursor() as cur:
       # создание таблиц
            cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                firstname VARCHAR(40),
                lastname VARCHAR(40),
                email VARCHAR(255)
                );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phons(
                id SERIAL PRIMARY KEY,
                ph_number VARCHAR(20) NOT NULL,
                client_id INTEGER NOT NULL REFERENCES clients(id)
                ON DELETE CASCADE
                );
            """)
            x.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    # добавление клиента
    with conn as x:
        with x.cursor() as cur:
            cur.execute("""
                    INSERT INTO clients(firstname, lastname, email) VALUES(%s, %s, %s)
                    RETURNING id;
                    """, (first_name, last_name, email))

            print(f'New id Clients: {cur.fetchone()}')

def add_phone(conn, client_id, phone):
    # добавление телефонного номера для клиента
    with conn as x:
        with x.cursor() as cur:
            cur.execute("""
            INSERT INTO phons(ph_number, client_id)
             VALUES(%s, %s) RETURNING id;
            """, (phone, client_id))
            print(f'New id Phones: {cur.fetchone()}')

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    # изменить данные о клиенте
    with conn as x:
        with x.cursor() as cur:
            if first_name is not None:
                cur.execute("""
                UPDATE clients SET firstname=%s WHERE id=%s;
                """, (first_name, client_id))
            if last_name is not None:
                cur.execute("""
                UPDATE clients SET lastname=%s WHERE id=%s;
                """, (last_name, client_id))
            if first_name is not None:
                cur.execute("""
                UPDATE clients SET firstname=%s WHERE id=%s;
                """, (first_name, client_id))
            if email is not None:
                cur.execute("""
                UPDATE clients SET email=%s WHERE id=%s;
                """, (email, client_id))
            if phone is not None:
                cur.execute("""
                UPDATE phons SET ph_number=%s WHERE client_id=%s;
                """, (phone, client_id))

            cur.execute("""SELECT * FROM clients;""")
            print(cur.fetchall())

            cur.execute("""SELECT * FROM phons;""")
            print(cur.fetchall())

def delete_phone(conn, client_id, phone):
    # удаление телефона для существующего клиента
    with conn as x:
        with x.cursor() as cur:
            cur.execute("""
            DELETE FROM phons WHERE client_id=%s and ph_number =%s;
            """, (client_id, phone))

            cur.execute("""SELECT * FROM phons;""")
            print(cur.fetchall())


def delete_client(conn, client_id: int):
    # удаление существующего клиента
    with conn as x:
        with x.cursor() as cur:
            cur.execute("""
            DELETE FROM clients WHERE id=%s;
            """, (client_id,))

            cur.execute("""SELECT * FROM clients;""")
            print(cur.fetchall())

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    # поиск клиента по его данным: имени, фамилии, email или  телефону
    with conn as x:
        with x.cursor() as cur:
            cur.execute("""
                        SELECT c.id FROM clients as c
                        JOIN phons ON c.id = client_id
                        WHERE firstname=%s OR
                              lastname=%s OR
                              email=%s OR
                              ph_number=%s;
                        """, (first_name, last_name, email, phone))
            return cur.fetchone()[0]


if __name__ == '__main__':
    # создание БД
    conn = psycopg2.connect(database="hw_clients", user="postgres", password="1201")
    create_db(conn)

    # добавление клиента
    first_name, last_name, email = 'Name5', 'Lastname5', 'mail5@mail.ru'
    add_client(conn, first_name, last_name, email, phones=None)

    # добавление телефонного номера для клиента
    phone = '+7 905 555 55 55'
    client_id = 5
    add_phone(conn, client_id, phone)

   # изменение данных о клиенте
    client_id = 5
    change_client(conn, client_id, first_name='Name5 new', last_name='Lastname5 new', email=None, phone = '+7 555 055 55 55')

   # удаление телефона для существующего клиента
    client_id = 5
    phone = '+7 111 333 44 55'
    delete_phone(conn, client_id, phone)

   # удаление существующего клиента
    client_id = 5
    delete_client(conn, client_id)

   # поиск клиента
    answer = find_client(conn, first_name=None, last_name=None, email=None, phone='+7 144 044 04 04')
    print(f"запросу соответствует id клиента: {answer}")

    conn.close()