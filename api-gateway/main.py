from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Define the base URLs for your microservices
AUTHENTICATION_SERVICE_URL = "http://192.168.0.130:5000"
PATIENT_SERVICE_URL = "http://192.168.0.130:5001"
EMPLOYEE_SERVICE_URL = "http://192.168.0.130:5002"
APPOINTMENT_SERVICE_URL = "http://192.168.0.130:5003"
INVENTORY_SERVICE_URL = "http://192.168.0.130:5007"

@app.api_route("/patient/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE","PATCH"])
async def users_service_proxy(path_name: str, request: Request):
    print(path_name)
    method = request.method
    body = await request.body()
    print(body)
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{PATIENT_SERVICE_URL}/patient/{path_name}", content=body, headers=request.headers)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

@app.api_route("/doctor/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE","PATCH"])
async def users_service_proxy(path_name: str, request: Request):
    print(path_name)
    method = request.method
    body = await request.body()
    print(body)
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{EMPLOYEE_SERVICE_URL}/doctor/{path_name}", content=body, headers=request.headers)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

@app.api_route("/employee/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE","PATCH"])
async def users_service_proxy(path_name: str, request: Request):
    print(path_name)
    method = request.method
    body = await request.body()
    print(body)
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{EMPLOYEE_SERVICE_URL}/employee/{path_name}", content=body, headers=request.headers)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

@app.api_route("/authentication/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def users_service_proxy(path_name: str, request: Request):
    print(path_name)
    method = request.method
    body = await request.body()
    print(body)
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{AUTHENTICATION_SERVICE_URL}/authentication/{path_name}", content=body, headers=request.headers)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

@app.api_route("/appointment/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE","PATCH"])
async def users_service_proxy(path_name: str, request: Request):
    print(path_name)
    method = request.method
    body = await request.body()
    print(body)
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{APPOINTMENT_SERVICE_URL}/appointment/{path_name}", content=body, headers=request.headers)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

@app.api_route("/inventory/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE","PATCH"])
async def users_service_proxy(path_name: str, request: Request):
    print(path_name)
    method = request.method
    body = await request.body()
    print(body)
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{INVENTORY_SERVICE_URL}/inventory/{path_name}", content=body, headers=request.headers)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
