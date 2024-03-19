import sqlite3

# Create a connection to the database
connection = sqlite3.connect('DATA.db')

# Create a cursor object
cursor = connection.cursor()

# Create a table 
table_info = "CREATE TABLE DATA(NAME VARCHAR(25), DEPARTMENT VARCHAR(25), POSITION VARCHAR(25), SALARY INT);"

cursor.execute(table_info)

# Insert data into the table
cursor.execute('''INSERT INTO DATA VALUES('John Doe', 'Engineering', 'Software Engineer', 80000)''')
cursor.execute('''INSERT INTO DATA VALUES('Jane Smith', 'Marketing', 'Marketing Manager', 90000)''')
cursor.execute('''INSERT INTO DATA VALUES('Michael Johnson', 'Sales', 'Sales Representative', 75000)''')
cursor.execute('''INSERT INTO DATA VALUES('Emily Brown', 'Finance', 'Financial Analyst', 85000)''')
cursor.execute('''INSERT INTO DATA VALUES('David Lee', 'Human Resources', 'HR Manager', 95000)''')

print("Employee Data:")

# Select and print data from the table
data = cursor.execute('''SELECT * FROM DATA''')

for row in data:
    print(row)

connection.commit()
connection.close()