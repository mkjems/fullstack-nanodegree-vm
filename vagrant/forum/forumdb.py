#
# Database access functions for the web forum.

import time
import datetime
import psycopg2

# Database connection
DB = []


def GetConnection():
    connection = psycopg2.connect("dbname=forum")
    cursor = connection.cursor()
    return (connection, cursor)


# Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    conn, cursor = GetConnection()
    cursor.execute("SELECT * FROM posts order by time desc;")
    results = cursor.fetchall()
    conn.close()

    db_posts = [{
        'content': str(row[0]),
        'time': datetime.datetime.strptime(
            str(row[1]), '%Y-%m-%d %H:%M:%S.%f').strftime(
            '%d, %b %Y %H:%M:%S')
    } for row in results]

    return db_posts


# Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    conn, cursor = GetConnection()
    cursor.execute("INSERT INTO posts (content) VALUES ('{}')".format(content))
    conn.commit()
    conn.close()

    t = time.strftime('%c', time.localtime())
    DB.append((t, content))
