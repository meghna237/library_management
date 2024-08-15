#SOURCE CODE

import time
import tabulate as t
import mysql.connector as m
def password():
    import pickle as p
    f=open('password.dat','rb')
    x=p.load(f)
    f.close()
    return x
def add_book():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    b_id=int(input("Enter the Book Id:"))
    name=input("Enter the the name of the book:")
    auth=input("Enter the Author :")
    gen=input("Enter your Genre:")
    copies=int(input("Enter the number of copies:"))
    q="insert into libdata values ({},'{}','{}','{}',{},0,{})".format(b_id,name,auth,gen,copies,copies)
    cur.execute(q)
    c.commit()
def remove_book():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    b_id=int(input('Enter the book_id of book to be removed:'))
    q="delete from libdata where Book_id={}".format(b_id)
    cur.execute(q)
    c.commit()
def modify_book():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    b_id=int(input('Enter book_id:'))
    q="select exists(select * from libdata where book_id={})".format(b_id)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        name=input('Enter name of book:')
        auth=input('Enter name of author:')
        gen=input('Enter the genre:')
        copies=int(input('Total no of copies:'))
        ava=int(input('Total no of copies available:'))
        q1="update libdata set bookname ='{}',genre='{}',no_of_copies='{}',no_available='{}',author='{}' where book_id={}".format(name,gen,copies,ava,auth,b_id)
        cur.execute(q1)
        c.commit()
    else:
        print('The details of ',b_id,' does not exist')
def add_user():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    u_id=input('Enter user id:')
    q="select exists(select * from user_data where user_id='{}')".format(u_id)
    cur.execute(q)
    e=cur.fetchall()
    if e!=[(1,)]:
        name=input('Enter name:')
        y=input('Has user issued a book(y/n):')
        if y in('y','Y'):
            b_id=int(input('Enter book id:'))
            q2="select exists(select * from libdata where book_id={})".format(b_id)
            cur.execute(q2)
            e1=cur.fetchall()
            if e1==[(1,)]:
                q3="update libdata set no_available=no_available-1, popularity=popularity+1 where book_id={}".format(b_id)
                cur.execute(q3)
                c.commit()
                st=input('Is user student or teacher(s/t):')
                if st in ('s','S'):
                    cls=int(input('Enter the class:'))
                    divi=input('Enter the division:')
                    q1="insert into user_data values('{}','{}','S','{}','{}',{},curdate(),date_add(curdate(), interval 7 day))".format(u_id,name,cls,divi,b_id)
                    cur.execute(q1)
                    c.commit()
                elif st in('t','T'):
                    q1="insert into user_data values('{}','{}','T',null,null,{},curdate(),date_add(curdate(),interval 7 day))".format(u_id,name,b_id)
                    cur.execute(q1)
                    c.commit()
                else:
                    print('Your choice is invalid')
        elif y in('n','N'):
            st=input('Is user student or teacher(s/t):')
            if st in('s','S'):
                cls=int(input('Enter the class:'))
                divi=input('Enter the division:')
                q2="insert into user_data values('{}','{}','S','{}','{}',null,null,null)".format(u_id,name,cls,divi)
                cur.execute(q2)
                c.commit()
            elif st in('t','T'):
                q2="insert into user_data values('{}','{}','T',null,null,null,null,null)".format(u_id,name)
                cur.execute(q2)
                c.commit()
        else:
            print('Your choice is not valid')
def remove_user():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    u_id=input('Enter the user_id to be deleted:')
    q="select exists(select * from user_data where user_id='{}')".format(u_id)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        q1="select exists(select * from user_data where user_id='{}' and book_id=null)".format(u_id)
        cur.execute(q1)
        e2=cur.fetchall()
        if e2!=[(1,)]:
            q2="update user_data u, libdata l set no_available=no_available+1 where user_id='{}' and u.book_id=l.book_id".format(u_id)
            cur.execute(q2)
            c.commit()
        q3="delete from user_data where user_id='{}'".format(u_id)
        cur.execute(q3)
        c.commit()
def available_books():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    q='select * from libdata where no_available!=0'
    cur.execute(q)
    rows=cur.fetchall()
    h=["Book id","Book name","Author","Genre","No of copies","Popularity","No of copies available"]
    print(t.tabulate(rows,headers=h,tablefmt="pretty"))
def modify_user():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    u_id=input('Enter the user_id:')
    q="select exists(select * from user_data where user_id='{}')".format(u_id)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        name=input('Enter the name:')
        y=input('Has the user issued the book(y/n):')
        if y in('y','Y'):
            b_id=int(input('Enter book_id:'))
            q2="select exists(select * from libdata where book_id={})".format(b_id)
            cur.execute(q2)
            e1=cur.fetchall()
            if e1==[(1,)]:
                q3="update libdata set no_available=no_available-1, popularity=popularity+1 where book_id={}".format(b_id)
                cur.execute(q3)
                c.commit()
                st=input('Is user student or teacher:')
                if st in ('s','S'):
                    cls=int(input('Enter the class:'))
                    divi=input('Enter the division:')
                    q1="update user_data set name='{}',student_teacher='S',class='{}',divi='{}',book_id={},issue_date=curdate(),return_date=date_add(curdate(),interval 7 day) where user_id='{}'".format(name,cls,divi,b_id,u_id)
                    cur.execute(q1)
                    c.commit()
                elif st in ('t','T'):
                    q1="update user_data set name='{}',student_teacher='T',class=null,divi=null,book_id={},issue_date=curdate(),return_date=date_add(curdate(),interval 7 day) where user_id='{}'".format(name,b_id,u_id)
                    cur.execute(q1)
                    c.commit()
                else:
                    print('Your choice is unavailable')
        elif y in ('n','N'):
            st=input('Is user student or teacher:')
            if st in ('s','S'):
                cls=int(input('Enter class:'))
                divi=input('Enter the division:')
                q2="update user_data set name='{}',student_teacher='S',class='{}',divi='{}',book_id=null,issue_date=null,return_date=null where user_id='{}'".format(name,cls,divi,u_id)
                cur.execute(q2)
                c.commit()
            elif st in ('t','T'):
                q2="update user_data set name='{}',student_teacher='T',class=null,divi=null,book_id=null,issue_date=null,return_date=null where user_id='{}'".format(name,u_id)
                cur.execute(q2)
                c.commit()
            else:
                print('Your choice is unavailable')
        else:
            print('Your choice is unavailable')
    else:
        print('Details of user does not exists')
def user_issue_details():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    b_id=int(input('Enter book_id:'))
    q="select exists(select * from libdata where book_id={})".format(b_id)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        q2="select exists(select * from user_data natural join libdata where book_id={})".format(b_id)
        cur.execute(q2)
        e2=cur.fetchall()
        if e2==[(1,)]:
            q3="select * from user_data natural join libdata where book_id={}".format(b_id)
            cur.execute(q3)
            l=cur.fetchall()
            h=["Book Id","User id","Name","Student/Teacher","Class","Division","Issue date","Return date","Book name","Author","Genre","No of copies","Popularity","No of books available"]
            print(t.tabulate(l,headers=h,tablefmt="pretty"))
        else:
            print("No one has issued the book")
    else:
        print('Details of ',b_id,'does not exist')
def late_return():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    q="select exists(select * from user_data where curdate()> return_date)"
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        q2= "select * from user_data where curdate()> return_date"  
        cur.execute(q2)
        l=cur.fetchall()
        h=["User id","Name","Student/Teacher","Class","Division","Book id","Issue date","Return date"]
        print(t.tabulate(l,headers=h,tablefmt="pretty"))
    else:
        print("Everyone has returned the book on time")
def get_book():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    u_id=input('Enter user_id:')
    q="select exists(select * from user_data where user_id='{}')".format(u_id)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        b_id=int(input('Enter id of book to be issued:'))
        q1="select exists(select * from libdata where book_id={})".format(b_id)
        cur.execute(q1)
        e1=cur.fetchall()
        if e1==[(1,)]:
            q2="update user_data set book_id={},issue_date=curdate(),return_date=date_add(curdate(), interval 7 day) where user_id='{}' ".format(b_id,u_id)
            cur.execute(q2)
            c.commit()
            q3="update libdata set no_available=no_available-1,popularity=popularity+1 where book_id={}".format(b_id)
            cur.execute(q3)
            c.commit()
        else:
            print("Details of book with book id", b_id,"does not exist")
    else:
        print('Details of ',u_id,'does not exists')
def return_book():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    u_id=input('Enter user_id:')
    q="select exists(select * from user_data where user_id='{}')".format(u_id)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        q1="select exists(select * from user_data where user_id='{}' and book_id is null)".format(u_id)
        cur.execute(q1)
        e1=cur.fetchall()
        if e1==[(1,)]:
            print("You have no book to return")
        else:
            q2="update libdata l, user_data u set u.book_id=null, issue_date=null,return_date=null, no_available=no_available+1 where user_id='{}'".format(u_id)
            cur.execute(q2)
            c.commit()
            print('Your book has been returned')
    else:
        print("The details of user",u_id,"does not exist")
def search_by_title():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    p=input('Enter the bookname to be searched:')
    q="select exists(select * from libdata where bookname like '%{}%' )".format(p)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        q2="select * from libdata where bookname like '%{}%'".format(p)
        cur.execute(q2)
        d=cur.fetchall()
        h=["Book id","Book Name","Author","Genre","No of copies","Popularity","No of available books"]
        print(t.tabulate(d,headers=h,tablefmt="pretty"))
    else:
        print('The book you are searching for is not available in the library')
def search_by_author():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    a=input('Enter name of the author:')
    q="select exists(select * from libdata where author like '%{}%')".format(a)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        q="select * from libdata where author like '%{}%'".format(a)
        cur.execute(q)
        l=cur.fetchall()           
        h=["Book id","Book name","Author","Genre","No of copies","Popularity","No of available copies"]
        print(t.tabulate(l,headers=h,tablefmt="pretty"))
    else:
        print('The books from this author are not there in this library')
def search_by_genre():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    a=input('Enter name of the genre:')
    q="select exists(select * from libdata where genre like '%{}%')".format(a)
    cur.execute(q)
    e=cur.fetchall()
    if e==[(1,)]:
        q="select * from libdata where genre like '%{}%'".format(a)
        cur.execute(q)
        l=cur.fetchall()           
        h=["Book id","Book name","Author","Genre","No of copies","Popularity","No of copiews available"]
        print(t.tabulate(l,headers=h,tablefmt="pretty"))
    else:
        print('The books from this genre are not there in this library')
def popular_book():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    q="select * from libdata order by popularity desc"
    cur.execute(q)
    l=cur.fetchmany(20)
    print("The 20 most popular books are")
    h=["Book id","Book name","Author","Genre","No of copies","Popularity","No of books available"]
    print(t.tabulate(l,headers=h,tablefmt="pretty"))
def available_genre():
    import mysql.connector as m
    c=m.connect(host='localhost',user='root',password='free13lue13irds',charset='utf8',database='crs')
    cur=c.cursor()
    q="select genre, count(*) from libdata group by genre"
    cur.execute(q)
    l=cur.fetchall()
    print("The available genres are")
    h=["Genre","No of books"]
    print(t.tabulate(l,headers=h,tablefmt="pretty"))
while True:
    print('                MENU            ')
    print('1.Admin')
    print('2.User')
    print('3.Exit')
    s=int(input('Choose your designation:'))
    if s==1:
        c=False
        for i in range(3):
            a=input("Enter the password:")
            b=password()
            if a==b:
                c=True
                x='y'
                break
            else:
                print("Wrong password")
        while x in ('y','Y'):
            print("                 MENU                  ")
            print("1) Add a new book")
            print("2) Remove a book")
            print("3) Change details of a book")
            print("4) Add a new user")
            print("5) Remove a user")
            print("6) Modify details of a user")
            print("7) View available books")
            print("8) Details of users who issued a book")
            print("9) Details of users who haven't returned their book in time")
            u=int(input('Enter the choice:'))
            if u==1:
                add_book()
            elif u==2:
                remove_book()
            elif u==3:
                modify_book()
            elif u==4:
                add_user()
            elif u==5:
                remove_user()
            elif u==6:
                modify_user()
            elif u==7:
                available_books()
            elif u==8:
                user_issue_details()
            elif u==9:
                late_return()
            else:
                print('Your choice is unavailable')
            x=input("Do you want to continue as admin(y/n):")
        if c==False:
            print("You have run out of tries. Please try again later.")
    elif s==2:
        while True:
            print('                MENU                  ')
            print('1.Issue a book')
            print('2.Return a book')
            print('3.Search a book')
            print('4.Search for author')
            print('5.Search for genre')
            print('6.View available books')
            print('7.Most popular books')
            print('8.View available genre')
            u=int(input('Enter the choice:'))
            if u==1:
                get_book()
            elif u==2:
                return_book()
            elif u==3:
                search_by_title()
            elif u==4:
                search_by_author()
            elif u==5:
                search_by_genre()
            elif u==6:
                available_books()
            elif u==7:
                popular_book()
            elif u==8:
                available_genre()
            else:
                print("Your choice is unavailable")
            x=input("Do you want to continue as user(y/n):")
            if x not in('y','Y'):
                break
    elif s==3:
        break
    else:
        print("Your choice is invalid")
print("Thank You")





#OUTPUT

'''                MENU            
1.Admin
2.User
3.Exit
Choose your designation:1
Enter the password:makkusquad
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:1
Enter the Book Id:100005
Enter the the name of the book:The Hobbit
Enter the Author :J R R Tolkien
Enter your Genre:fiction
Enter the number of copies:2
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:3
Enter book_id:10003
The details of  10003  does not exist
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:7
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| Book id |        Book name         |     Author     |         Genre         | No of copies | Popularity | No of copies available |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| 100000  |    The Da Vinci Code     |   Dan Brown    |   mystery thriller    |      2       |     0      |           2            |
| 100001  |        In 27 Days        | Alison Gervais |        Fantasy        |      2       |     0      |           2            |
| 100002  | Adventures of Tom Sawyer |   Mark Twain   | Children's Literature |      4       |     0      |           4            |
| 100003  |    The Bad Boy's Girl    |  Blair Holden  |      Young Adult      |      1       |     0      |           1            |
| 100004  |     The Ivory Throne     | Manu S Pillai  |      Non fiction      |      2       |     0      |           2            |
| 100005  |        The Hobbit        | J R R Tolkien  |        fiction        |      2       |     0      |           2            |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:3
Enter book_id:100005
Enter name of book:The Hobbit
Enter name of author:J R R Tolkien
Enter the genre:Fantasy
Total no of copies:3
Total no of copies available:3
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:7
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| Book id |        Book name         |     Author     |         Genre         | No of copies | Popularity | No of copies available |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| 100000  |    The Da Vinci Code     |   Dan Brown    |   mystery thriller    |      2       |     0      |           2            |
| 100001  |        In 27 Days        | Alison Gervais |        Fantasy        |      2       |     0      |           2            |
| 100002  | Adventures of Tom Sawyer |   Mark Twain   | Children's Literature |      4       |     0      |           4            |
| 100003  |    The Bad Boy's Girl    |  Blair Holden  |      Young Adult      |      1       |     0      |           1            |
| 100004  |     The Ivory Throne     | Manu S Pillai  |      Non fiction      |      2       |     0      |           2            |
| 100005  |        The Hobbit        | J R R Tolkien  |        Fantasy        |      3       |     0      |           3            |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:4
Enter user id:S3426
Enter name:Emmit
Has user issued a book(y/n):n
Is user student or teacher(s/t):s
Enter the class:11
Enter the division:B
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:6
Enter the user_id:S9203
Details of user does not exists
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:6
Enter the user_id:S3426
Enter the name:Emmit
Has the user issued the book(y/n):y
Enter book_id:100001
Is user student or teacher:s
Enter the class:11
Enter the division:A
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:7
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| Book id |        Book name         |     Author     |         Genre         | No of copies | Popularity | No of copies available |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| 100000  |    The Da Vinci Code     |   Dan Brown    |   mystery thriller    |      2       |     1      |           1            |
| 100001  |        In 27 Days        | Alison Gervais |        Fantasy        |      2       |     1      |           1            |
| 100002  | Adventures of Tom Sawyer |   Mark Twain   | Children's Literature |      4       |     0      |           4            |
| 100003  |    The Bad Boy's Girl    |  Blair Holden  |      Young Adult      |      1       |     0      |           1            |
| 100004  |     The Ivory Throne     | Manu S Pillai  |      Non fiction      |      2       |     0      |           2            |
| 100005  |        The Hobbit        | J R R Tolkien  |        Fantasy        |      3       |     0      |           3            |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:9
+---------+-------+-----------------+-------+----------+---------+------------+-------------+
| User id | Name  | Student/Teacher | Class | Division | Book id | Issue date | Return date |
+---------+-------+-----------------+-------+----------+---------+------------+-------------+
|  S4849  | Kaden |        S        |   9   |    C     | 100000  | 2021-03-01 | 2021-03-08  |
+---------+-------+-----------------+-------+----------+---------+------------+-------------+
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:8
Enter book_id:100000
+---------+---------+-------+-----------------+-------+----------+------------+-------------+-------------------+-----------+------------------+--------------+------------+-----------------------+
| Book Id | User id | Name  | Student/Teacher | Class | Division | Issue date | Return date |     Book name     |  Author   |      Genre       | No of copies | Popularity | No of books available |
+---------+---------+-------+-----------------+-------+----------+------------+-------------+-------------------+-----------+------------------+--------------+------------+-----------------------+
| 100000  |  S4849  | Kaden |        S        |   9   |    C     | 2021-03-01 | 2021-03-08  | The Da Vinci Code | Dan Brown | mystery thriller |      2       |     1      |           1           |
+---------+---------+-------+-----------------+-------+----------+------------+-------------+-------------------+-----------+------------------+--------------+------------+-----------------------+
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:5
Enter the user_id to be deleted:s4849
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:7
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| Book id |        Book name         |     Author     |         Genre         | No of copies | Popularity | No of copies available |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| 100000  |    The Da Vinci Code     |   Dan Brown    |   mystery thriller    |      2       |     1      |           2            |
| 100001  |        In 27 Days        | Alison Gervais |        Fantasy        |      2       |     1      |           1            |
| 100002  | Adventures of Tom Sawyer |   Mark Twain   | Children's Literature |      4       |     0      |           4            |
| 100003  |    The Bad Boy's Girl    |  Blair Holden  |      Young Adult      |      1       |     0      |           1            |
| 100004  |     The Ivory Throne     | Manu S Pillai  |      Non fiction      |      2       |     0      |           2            |
| 100005  |        The Hobbit        | J R R Tolkien  |        Fantasy        |      3       |     0      |           3            |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
Do you want to continue as admin(y/n):y
                 MENU                  
1) Add a new book
2) Remove a book
3) Change details of a book
4) Add a new user
5) Remove a user
6) Modify details of a user
7) View available books
8) Details of users who issued a book
9) Details of users who haven't returned their book in time
Enter the choice:2
Enter the book_id of book to be removed:100005
Do you want to continue as admin(y/n):n
                MENU            
1.Admin
2.User
3.Exit
Choose your designation:2
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:1
Enter user_id:T4502
Enter id of book to be issued:100004
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:2
Enter user_id:S3426
Your book has been returned
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:2
Enter user_id:S3426
You have no book to return
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:3
Enter the bookname to be searched:Ivory Throne
+---------+------------------+---------------+-------------+--------------+------------+-----------------------+
| Book id |    Book Name     |    Author     |    Genre    | No of copies | Popularity | No of available books |
+---------+------------------+---------------+-------------+--------------+------------+-----------------------+
| 100004  | The Ivory Throne | Manu S Pillai | Non fiction |      2       |     1      |           2           |
+---------+------------------+---------------+-------------+--------------+------------+-----------------------+
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:3
Enter the bookname to be searched:Hobbit
The book you are searching for is not available in the library
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:4
Enter name of the author:Dan
+---------+-------------------+-----------+------------------+--------------+------------+------------------------+
| Book id |     Book name     |  Author   |      Genre       | No of copies | Popularity | No of available copies |
+---------+-------------------+-----------+------------------+--------------+------------+------------------------+
| 100000  | The Da Vinci Code | Dan Brown | mystery thriller |      2       |     1      |           2            |
+---------+-------------------+-----------+------------------+--------------+------------+------------------------+
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:4
Enter name of the author:J K Rowling
The books from this author are not there in this library
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:5
Enter name of the genre:horror
The books from this genre are not there in this library
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:5
Enter name of the genre:fantasy
+---------+------------+----------------+---------+--------------+------------+-------------------------+
| Book id | Book name  |     Author     |  Genre  | No of copies | Popularity | No of copiews available |
+---------+------------+----------------+---------+--------------+------------+-------------------------+
| 100001  | In 27 Days | Alison Gervais | Fantasy |      2       |     1      |            2            |
+---------+------------+----------------+---------+--------------+------------+-------------------------+
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:6
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| Book id |        Book name         |     Author     |         Genre         | No of copies | Popularity | No of copies available |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
| 100000  |    The Da Vinci Code     |   Dan Brown    |   mystery thriller    |      2       |     1      |           3            |
| 100001  |        In 27 Days        | Alison Gervais |        Fantasy        |      2       |     1      |           2            |
| 100002  | Adventures of Tom Sawyer |   Mark Twain   | Children's Literature |      4       |     0      |           5            |
| 100003  |    The Bad Boy's Girl    |  Blair Holden  |      Young Adult      |      1       |     0      |           2            |
| 100004  |     The Ivory Throne     | Manu S Pillai  |      Non fiction      |      2       |     1      |           2            |
+---------+--------------------------+----------------+-----------------------+--------------+------------+------------------------+
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:7
The 20 most popular books are
+---------+--------------------------+----------------+-----------------------+--------------+------------+-----------------------+
| Book id |        Book name         |     Author     |         Genre         | No of copies | Popularity | No of books available |
+---------+--------------------------+----------------+-----------------------+--------------+------------+-----------------------+
| 100000  |    The Da Vinci Code     |   Dan Brown    |   mystery thriller    |      2       |     1      |           3           |
| 100001  |        In 27 Days        | Alison Gervais |        Fantasy        |      2       |     1      |           2           |
| 100004  |     The Ivory Throne     | Manu S Pillai  |      Non fiction      |      2       |     1      |           2           |
| 100002  | Adventures of Tom Sawyer |   Mark Twain   | Children's Literature |      4       |     0      |           5           |
| 100003  |    The Bad Boy's Girl    |  Blair Holden  |      Young Adult      |      1       |     0      |           2           |
+---------+--------------------------+----------------+-----------------------+--------------+------------+-----------------------+
Do you want to continue as user(y/n):y
                MENU                  
1.Issue a book
2.Return a book
3.Search a book
4.Search for author
5.Search for genre
6.View available books
7.Most popular books
8.View available genre
Enter the choice:8
The available genres are
+-----------------------+-------------+
|         Genre         | No of books |
+-----------------------+-------------+
|   mystery thriller    |      1      |
|        Fantasy        |      1      |
| Children's Literature |      1      |
|      Young Adult      |      1      |
|      Non fiction      |      1      |
+-----------------------+-------------+
Do you want to continue as user(y/n):n
                MENU            
1.Admin
2.User
3.Exit
Choose your designation:3
Thank You
>>> '''
