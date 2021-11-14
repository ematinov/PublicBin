import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host='localhost',
        port=8081,
        reload=True,
        workers=2,
    )