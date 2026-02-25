from model import(Base, session, Book, engine)
import datetime
import csv, time



# menu
def menu():
    while True:
        print(''' 
              \nPROGRAMMING BOOKS
             \r1. Add book
              \r2. View all books
              \r3. Search for books
              \r4. Book Analysis
              \r5. Exit
              ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above
                  \r A number from 1 - 5.
                  \rPress enter to try again.
                  ''')
def submenu():
     while True:
        print(''' 
             \r1. Edit
              \r2. Delete
              \r3. Return to main menu''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above
                  \r A number from 1 - 3.
                  \r Press enter to try again.
                  ''')
 
#cleaned_id:
def clean_id(id_str,options):
    try:
        book_id = int(id_str)
    except ValueError:
        input(''' 
              \n ***** ID ERROR *****
              \r The ID should be a number and within the specified range
              \r Press enter to try again
              ''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(''' 
                  \n ID error
                  \n Press enter to try again
                  ''')
            time.sleep(1.5)
            return
    



#cleaned_price
def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        print(''' 
              \n *** Price Error ***
              \r Price should be a number without a currency symbol exp: 10.99
              ''')
    else:
        return int(price_float * 100)
    

# cleaned_date
def clean_date(date_str):
     months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
     split_date  = date_str.split(' ')
     try:
        month = int(months.index(split_date[0]) + 1)
        year = int(split_date[2])
        day = int(split_date[1].split(',')[0])
        return_date = datetime.date(year,month,day)
     except ValueError:
        input(''' 
              \n *** DATE ERROR ***
              \r The date format should include a valid Month Day, Year
              \r ex: January 13, 2022
              \r Press enter to continue ''')
        return
     else:
         return return_date     

def edit_check(column_name, current_value):
    print(f'\n**** EDIT {column_name} ****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name =='Date':
        print(f'\rCurrent_Value : {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'\rCurrent Value: {current_value}') 
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')

    

#add csv
def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            #  print(row)
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()
             
    


# app
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # Add book]
            title = input('Title: ')
            author  =input('Author: ')
            date_error = True
            while date_error: 
                published_date = input('Published date: (ex: "November 12, 2019"): ')
                published_date = clean_date(published_date)
                if type(published_date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price =input('Price: (ex: 35.96) ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=published_date, price = price)
            session.add(new_book)
            session.commit()
            time.sleep(1.6)
            print('Book added successfully!')
                
    
        elif choice == '2':
            # view books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\n Press enter to return to the main menu')
        elif choice == '3':
            # search book
            id_option = []
            for book in session.query(Book):
                id_option.append(book.id)
            id_error  = True
            while id_error:
                id_choice = input(f'''
                   \nId Options: {id_option}
                   \rBook id: ''')
                id_choice = clean_id(id_choice,id_option)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f''' 
                  \n{the_book.title} by {the_book.author}
                  \rPublished Date : {the_book.published_date}
                  \rPrice : ${the_book.price / 100}\n''')
            sub_choice = submenu()
            if sub_choice == '1':
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check('Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                time.sleep(1.7)
                print('Book updated successfully!')
            elif sub_choice == '2':
                # delete
                 session.delete(the_book)
                 session.commit()
                 time.sleep(1.6)
                 print('Book deleted successfully!')
                
           
        elif choice == '4':
            # book analysis
            pass
        else:
            print('GOODBYE')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # add_csv()
    app()
    # for  book in session.query(Book):
    #     print(book)
    
    