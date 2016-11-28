import sqlite3

def getFreshTable():
    connection = sqlite3.connect('parking_lot.db')
    
    cursor = connection.cursor()
    
    drop_table = "DROP TABLE IF EXISTS parking_lot_list"
    cursor.execute(drop_table)
    
    create_table = "CREATE TABLE parking_lot_list (id int, lot_name text, empty int, full int, mostlyEmpty int, mostlyFull int)"
    cursor.execute(create_table)
    
    lots = [
        (1, 'Parking Structure', 0, 0, 0, 0),
        (2, 'Lot B', 0, 0, 0, 0),
        (3, 'Lot E1', 0, 0, 0, 0),
        (4, 'Lot E2', 0, 0, 0, 0),
        (5, 'Lot F1', 0, 0, 0, 0),
        (6, 'Lot F2', 0, 0, 0, 0),
        (7, 'Lot F3', 0, 0, 0, 0),
        (8, 'Lot F4', 0, 0, 0, 0),
        (9, 'Lot F5', 0, 0, 0, 0),
        (10, 'Lot F8', 0, 0, 0, 0),
        (11, 'Lot F9', 0, 0, 0, 0),
        (12, 'Lot F10', 0, 0, 0, 0),
        (13, 'Lot H', 0, 0, 0, 0),
        (14, 'Lot J', 0, 0, 0, 0),
        (15, 'Lot M', 0, 0, 0, 0),
        (16, 'Paved Overflow Lot', 0, 0, 0, 0),
        (17, 'Parking Structure 2', 0, 0, 0, 0),
        (18, 'Lot U', 0, 0, 0, 0),
        (19, 'Unpaved Overflow Lot', 0, 0, 0, 0)
    ]
    
    insert_statement = "INSERT INTO parking_lot_list VALUES (?,?,?,?,?,?)"
    cursor.executemany(insert_statement, lots)
    
    drop_table = "DROP TABLE IF EXISTS last_update"
    
    cursor.execute(drop_table)
    
    create_table = "CREATE TABLE last_update (last_date_modified DATE)"
    
    cursor.execute(create_table)
    
    insert_date = "INSERT INTO last_update VALUES (CURRENT_DATE)"
    
    cursor.execute(insert_date)
    
    connection.commit()
    
    connection.close()
    
getFreshTable()