from fastapi import FastAPI
from app.routers import user, item, dinner_style, dinner_menu
import uvicorn

app = FastAPI()

app.include_router(user.router)
app.include_router(item.router)
app.include_router(dinner_style.router)
app.include_router(dinner_menu.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, log_level="info")
