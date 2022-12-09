from .metadata import description, tags_metadata, title_metadata, version_metadata, terms_metadata, contact_metadata, licence_metadata, ui_metadata
from .routers import rte_auth, rte_posts, rte_users, rte_votes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

server = FastAPI(title=title_metadata, description=description, version=version_metadata,
                 terms_of_service=terms_metadata, contact=contact_metadata, license_info=licence_metadata,
                 swagger_ui_parameters=ui_metadata, openapi_tags=tags_metadata, redoc_url=None)


origins = ["*"]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@server.get("/", tags=['Root'], include_in_schema=False)
async def root():
    return {"detail": "root"}

server.include_router(rte_auth.router)
server.include_router(rte_users.router)
server.include_router(rte_posts.router)
server.include_router(rte_votes.router)


# Create
# cursor.execute("""INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *; """, (post.title, post.content, post.published))
# post = cursor.fetchone()
# conn.commit()
# Get All
# cursor.execute("""SELECT * FROM posts ORDER BY id;""")
# post = cursor.fetchall()
# Get One
# cursor.execute("""SELECT * FROM posts WHERE id = %s; """, str(id))
# post = cursor.fetchone()
# Update
# cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *; """, (post.title, post.content, post.is_published, str(id)))
# data = cursor.fetchone()
# conn.commit()
# Delete
# cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *; """, str(id))
# post = cursor.fetchone()
# conn.commit()
