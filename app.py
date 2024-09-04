from datetime import datetime
from pymongo import MongoClient
from termcolor import colored

client = MongoClient("mongodb://localhost:27017/")

db = client['lms']
collection = db['book_info']

def insert_data():
    print(colored("""
            ---------- Enter the Book Details  ------------
            """, "yellow"))
    book_id = str(input("Enter the Book Id : "))
    if book_id == "":
        print(colored(" => Please enter the valid input .....", 'red'))
        book_id = str(input("Enter the Book Id : "))

    book_name = str(input("Enter the Book Name : "))
    if book_name == "":
        print(colored(" => Please enter the valid input .....", 'red'))
        book_name = str(input("Enter the Book Name : "))

    nfg_tag_id = str(input("Enter the nfg_tag_id : "))
    if nfg_tag_id == "":
        print(colored(" => Please enter the valid input .....", 'red'))
        nfg_tag_id = str(input("Enter the nfg_tag_id  : "))

    author_name = str(input("Enter the author Name : "))
    if author_name == "":
        print(colored(" => Please enter the valid input .....", 'red'))
        author_name = str(input("Enter the Author Name : "))

    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    data = {
        "book_id": book_id,
        "book_name": book_name,
        "nfg_tag_id": nfg_tag_id,
        "author_name": author_name,
        "date": date,
        "time_date": time
    }
    result = collection.insert_one(data)
    print(colored(f"Data was inserted into DB, Object Id {result.inserted_id}", 'green'))


def display():

    print(colored("------------- Display Page of Collection --------------\n", 'yellow'))

    print("List of collection Name & Choose the Collection Name\n")

    collection_list_name = db.list_collection_names()
    i = 0
    for coll in collection_list_name:
        i += 1
        print(f" {i} => {coll}")

    choose_coll = int(input("\nChoose the Collection Serial No  : ")) - 1
    collection_name = db[f"{collection_list_name[choose_coll]}"]
    coll_len = collection_name.count_documents({})
    if coll_len == 0:
        print(colored("No Data inserted the Collection...... ", 'red'))
    else:
        print(f"""
        ==> Collection Name : {collection_list_name[choose_coll]}
        ==> Database Name : {db.name}
        ==> Total No of data : {coll_len} 
        """)
        for coll_data in collection_name.find({}, {}):
            print(coll_data)



while True:

    print("""
    --------- Data entry for book ---------------
    1. insert data & Enter 1
    2. Display data &  Enter 2
    3. Close the entry
    """)

    option = int(input("Enter the option : "))
    if option == 1:
        insert_data()
    elif option == 2:
        display()
    elif option == 3:
        print("Thank you ..... ")
        break
    else:
        print("Enter the valid input option")




