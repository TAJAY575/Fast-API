from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange 
import uvicorn 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None 
    
    
my_posts = [{"title" : "title of post 1" , "content": "content of post 1", "id" : 1}, 
            {"title" : "favorite foods", "content" : "i like pizza", "id" : 2}]
    
    
def  find_post(id):
    for p in my_posts : 
        if p["id"] == id : 
            return p  

def find_index_post(id) :
    for i , p in enumerate(my_posts):
        if p['id'] == id:
            return i



@app.get("/")
def root():
    return {"Hello": "welcome to my api"}


@app.get("/posts")
def get_posts() :
    return {"data": my_posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def createpost(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post.dict())
    return {"data" : my_posts}

@app.get("/posts/{id}")
def get_post(id : int, response : Response):
    
    post = find_post(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    return {"post_detail" : post }


@app.delete ("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def Delete_post(id : int, ):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exsist")
    my_posts.pop(index)
    
    
@app.put ("/posts/{id}")
def update_post(id : int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exsist")

    post_dict = post.dict() 
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}

def start_server():
    print('Starting Server...')       

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8765,
        log_level="debug",
        reload=True,
    )

# To run the FastAPI app
if __name__ == "__main__":
    start_server()
    