# this project started by Ali 21-11-2022
import uvicorn

from api_gateway import app


if __name__ == "__main__":
    uvicorn.run(app)
