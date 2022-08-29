import uvicorn;
from fastapi import FastAPI, Response;
from fastapi.middleware.cors import CORSMiddleware;
from fastapi.responses import HTMLResponse;
from fastapi.staticfiles import StaticFiles;
from api import repos;

app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
);

app.include_router(repos.router);

@app.get('/', response_class=HTMLResponse)
def get_Index(response: Response):
    try:
        with open('app/index.html', 'r', encoding='utf8') as f:
            ret = f.read();
            f.close();
            return ret;
    except:
        response.status_code = 404;

if __name__ == '__main__':
    uvicorn.run('main:app', port=4810, log_level='info');