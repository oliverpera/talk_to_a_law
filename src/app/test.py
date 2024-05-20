import sqlite3

def print_tables(database_file):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # SQL-Abfrage zum Abrufen der Tabellennamen
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(query)

    # Tabellennamen ausgeben
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

    # Verbindung zur Datenbank schließen
    cursor.close()
    conn.close()
    
    
def print_collection_content(database_file):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    # SQL-Abfrage zum Abrufen des Inhalts der Tabelle "collections"
    query = "SELECT * FROM collections;"
    cursor.execute(query)
    # Inhalte ausgeben
    content = cursor.fetchall()
    for row in content:
        print(row,'\n')
    # Verbindung zur Datenbank schließen
    cursor.close()
    conn.close()



print_collection_content("src/resources/chromadb/chroma.sqlite3")
print_tables("src/resources/chromadb/chroma.sqlite3")