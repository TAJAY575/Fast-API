from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange 
import uvicorn 
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
app = FastAPI()


user= os.getenv("user")
password= os.getenv("password")

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    

while  True:
    try : 
        conn = psycopg2.connect(host= 'localhost', database ='postgres', user = user,
                                password = password, cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("INFO:\t Database connection was successful")
        break
    except Exception as error:
        print("INFO:\t Database connection fail")
        print("INFO: \t",error)
        time.sleep(2)
        


@app.get("/")
def root():
    return {"Hello": "welcome to my api"}


@app.get("/posts")
def get_posts() :
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING 
                   * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id : int, response : Response):
    
    cursor.execute(""" SELECT * FROM posts WHERE id= %s """,(str(id),))
    post = cursor.fetchone() 
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    return {"post_detail" : post }


@app.delete ("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def Delete_post(id : int, ):
    cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()  
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exist")
    
    
@app.put ("/posts/{id}")
def update_post(id : int, post: Post):
    cursor.execute(""" UPDATE posts SET title= %s, content =%s, published = %s WHERE id= %s   RETURNING *""", 
                (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()   
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with  id {id} does not exist")
    return {"data" : updated_post}

def start_server():
    try:
        print('Starting Server...')       

        uvicorn.run(
            "main:app",
            reload=True,
    )
    except Exception as e:
        print(f"Error starting server: {e}")

# To run the FastAPI app
if __name__ == "__main__":
    start_server()