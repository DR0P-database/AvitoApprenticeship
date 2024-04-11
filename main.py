import uvicorn


if __name__ == '__main__':
    uvicorn.run('banners_app.app:app', reload=True)
