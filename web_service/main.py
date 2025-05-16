from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

user_ips = []
groups = []

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/add")
def add(request: Request):
    ip = request.client.host
    user_ips.append(ip)
    
    return {"ips": user_ips}

@app.post("/create_group")
async def create_group(request: Request):
    data = await request.json()
    group_name = data.get("name")
    if group_name:
        groups.append(group_name)
        return {"groups": groups}
    return {"error": "No group name provided"}, 400

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
