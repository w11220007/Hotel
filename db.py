import mysql.connector
from mysql.connector import Error, errorcode
from werkzeug.security import generate_password_hash, check_password_hash

hostname = "localhost"
username = "root"
passwd = "data"
db = "HOTEL_DB"


def getConnection():
    try:
        conn = mysql.connector.connect(
            host=hostname, user=username, password=passwd, database=db
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or Password is not working")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return conn


class Model:
    def __init__(self):
        self.conn = getConnection()
        self.tbName = ""
        if self.conn != None:
            if self.conn.is_connected():
                self.dbcursor = self.conn.cursor()
            else:
                print("DBfunc error")

    def getAll(self, limit=1000):
        try:
            self.dbcursor.execute('select * from ' + self.tbName + ' limit ' + str(limit))
            myresult = self.dbcursor.fetchall()
        except Error as e:
            myresult = ()
        else:
            if self.dbcursor.rowcount == 0:
                myresult = ()
        return myresult

    

class Hotel(Model):
    def __init__(self):
        super().__init__()
        self.tbName = "hotel"
    
    def getById(self, id):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where HID = {}'.format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult
    
    def getDetailById(self, id):
        try:
            self.dbcursor.execute(' seclect H.*. .Hname ')
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult

    def addNew(self, hotel):
        try:
            self.dbcursor.execute("insert into "+ self.tbName +
                                " values (%s, %s, %s, %s, %s)",
                                    (hotel["HID"], hotel["HName"], hotel["Address"], hotel["Hotline"], hotel["Price"]))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True
    
    
    def update(self, hotel):
        try:
            self.dbcursor.execute("update "+ self.tbName +
                                " set Hname = %s, \
                                    Address = %s, \
                                    Hotline = %s, \
                                    Price = %s",
                                    (hotel["Hname"], hotel["Address"], hotel["Hotline"], hotel["Price"]))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True
    

class User(Model):
    def __init__(self, ):
        super().__init__()
        self.tbName = 'users'
            
    def addNew(self, user):
        try:
            self.dbcursor.execute('insert into '+ self.tbName + 
                                ' (username, email, password_hash, usertype) values (%s, %s, %s, %s)',
                                    (user['username'], user['email'], generate_password_hash(user['password']), user['usertype']))
            myresult = self.conn.commit()
        except Error as e:
#            print(e)
            return False   
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        return True
    
    def getById(self, id):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where id = {}'.format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult
    
    def getByUsername(self, username):
        try: 
            self.dbcursor.execute('select * from '+ self.tbName + ' where username = %s',(username,))

            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult

    def getByEmail(self, email):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where email = %s',(email,))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult
    
    def checkLogin(self, username, password):
        user = self.getByUsername(username)
        if user=='':
            user = self.getByEmail(username)
        if user:
            # print(user)
            if check_password_hash(user[3], password):
                return True
            
        return False


class Admin(User):
    
    def __init__(self):
        super().__init__()
        self.tbName = "admin"
    
    def getById(self, id):
        try:
            self.dbcursor.execute("select * from "+ self.tbName + " where CID = {}".format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult
    
    def getDetailById(self, id):
        try:
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult

    def addNew(self, customer):
        try:
            self.dbcursor.execute("insert into "+ self.tbName +
                                " values (%s, %s, %s, %s, %s)",
                                    (customer["CID"], customer["CName"], customer["CEmail"], customer["PNumber"], customer["DoR"]))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True
    
    
    def update(self, customer):
        try:
            self.dbcursor.execute("update "+ self.tbName +
                                " set CName = %s, \
                                    CEmail = %s, \
                                    PNumber = %s, \
                                    DoR = %s",
                                    (customer["CName"], customer["CEmail"], customer["PNumber"], customer["DoR"]))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True

class Customer(User):
    
    def __init__(self):
        super().__init__()
        self.tbName = "customer"
    
    def getByEmail(self, id):
        try:
            self.dbcursor.execute("select * from "+ self.tbName + " where CID = {}".format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult
    
    def getDetailById(self, id):
        try:
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        return myresult

    def addNew(self, customer):
        try:
            self.dbcursor.execute("insert into "+ self.tbName +
                                " values (%s, %s, %s, %s, %s)",
                                    (customer["CID"], customer["CName"], customer["CEmail"], customer["PNumber"], customer["DoR"]))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True
    
    
    def update(self, customer):
        try:
            self.dbcursor.execute("update "+ self.tbName +
                                " set CName = %s, \
                                    CEmail = %s, \
                                    PNumber = %s, \
                                    DoR = %s",
                                    (customer["CName"], customer["CEmail"], customer["PNumber"], customer["DoR"]))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True

class Room(Hotel):
    def __init__(self):
        super().__init__()
        self.tbName = "room"
        
    def getById(self, id):
        try:
            self.dbcursor.execute(' select * from '+ self.tbName + ' where RID = {}'.format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
                
        return myresult
    def getDetailById(self, id):
        try:
            self.dbcursor.execute('SELECT * FROM ' + self.tbName + ' WHERE RID = %s', (id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        return myresult
    
    def getPriceById(self, id):
        try:
            query = 'SELECT price FROM {} WHERE id = %s'.format(self.tbName)
            self.dbcursor.execute(query, (id,))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            return None
        else:
            if myresult:
                return myresult[0]  
            else:
                return None 
            
    def getAdressById(self, id):
        try:
            query = 'SELECT address FROM {} WHERE id = %s'.format(self.tbName)
            self.dbcursor.execute(query, (id,))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            return None
        else:
            if myresult:
                return myresult[0]  
            else:
                return None 
            
    def getAvailableRooms(self, check_in_date, check_out_date):
        try:
            query = '''
                SELECT t1.room_id 
                FROM rooms t1 
                LEFT OUTER JOIN booking_room t2 ON t1.id = t2.room_id 
                WHERE t2.room_id IS NULL 
                OR (t2.check_in_date > %s OR t2.check_out_date < %s)
            '''
            self.dbcursor.execute(query, (check_out_date, check_in_date))
            available_rooms = self.dbcursor.fetchall()
        except Error as e:
            print(e)
            return None
        else:
            if available_rooms:
                return [room[0] for room in available_rooms]
            else:
                return None

class Bookig(Model):
    def __init__(self):
        super().__init__()
        self.tbName = 'booking'
        
    def getByBookingId(self, booking_id):
        try:
            self.dbcursor.execute(' SELECT * FROM ' + self.tbName +  ' WHERE BookingID = %s', (booking_id))
            myresult = self.dbcurdor.fetchone()
        except Error as e:
            print(e)
            myresult =()
        return myresult  
    def getByCustomerId(self, customer_id):
        try:
            self.dbcursor.execute("SELECT * FROM " + self.tbName + " WHERE CustomerID = %s", (customer_id,))
            myresult = self.dbcursor.fetchall()
        except Error as e:
            print(e)
            myresult = ()
        
        return myresult

    def addNew(self, booking):
        try:
            self.dbcursor.execute("INSERT INTO " + self.tbName + " VALUES (%s, %s, %s, %s, %s, %s)",
                                    (booking["BookingID"], booking["CustomerID"], booking["RoomID"],
                                    booking["CheckInDate"], booking["CheckOutDate"], booking["Status"]))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def update(self, booking):
        try:
            self.dbcursor.execute("UPDATE " + self.tbName + " SET CustomerID = %s, RoomID = %s, \
                                    CheckInDate = %s, CheckOutDate = %s, Status = %s WHERE BookingID = %s",
                                    (booking["CustomerID"], booking["RoomID"], booking["CheckInDate"],
                                    booking["CheckOutDate"], booking["Status"], booking["BookingID"]))
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False
        
    def checkin(self, booking):
        try:
            self.dbcursor.execute(' SELECT DAYCHECKIN FROM ' + self.tbName + ' SET CheckInDate = %s, CheckOutDate = %s', 
                                booking[' CheckInDate'], booking[' CheckOutDate'])
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

