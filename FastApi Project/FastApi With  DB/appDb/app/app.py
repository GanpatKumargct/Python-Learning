from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


class post(BaseModel):
    title : str
    content :str
    published:bool


try:
    conn = psycopg2.connect(host='localhost', database='Employee', user='postgres', 
                            password ='0000', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Databases are connected successfully.")
except Exception as err:
    print("Connection failed ",err)



@app.get("/")
def hello():
    return "Welcome to FastAPI With DB "

@app.get("/getAll")
def get_post():
    cursor.execute("""select * from post""")
    posts = cursor.fetchall()

    return {"data": posts}

@app.post("/create")
def create_post(p:post):
    cursor.execute("""insert into post (title,content,published) values(%s, %s, %s) returning *""",
                   (p.title, p.content, p.published))
    
    conn.commit()
    new_post = cursor.fetchone()
    return {"data":new_post}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"data": post}

@app.put("/posts/{id}")
def update_post(id: int, post: post):
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (id,))
    # existing_post = cursor.fetchone()

    # if not existing_post:
    #     raise HTTPException(status_code=404, detail="Post not found")

    get_post_by_id(id)
    
    cursor.execute(
        """
        UPDATE post
        SET title = %s,
            content = %s,
            published = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            post.title or existing_post["title"],
            post.content or existing_post["content"],
            post.published if post.published is not None else existing_post["published"],
            id
        )
    )

    conn.commit()
    updated_post = cursor.fetchone()
    return {"data": updated_post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Post deleted successfully", "data": deleted_post}
