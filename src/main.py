from typing import Callable

import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import ORJSONResponse

from api.v1 import base_api
from core.config import app_settings, subnet_blacklist

app = FastAPI(
    title=app_settings.project_name,
    default_response_class=ORJSONResponse,
)


@app.middleware('http')
async def check_client_subnet(request: Request, call_next: Callable):
    client_ip = request.client.host
    from ipaddress import ip_address, ip_network
    client_ip = ip_address(client_ip)
    for subnet in subnet_blacklist:
        if client_ip in ip_network(subnet):
            return Response(status_code=status.HTTP_403_FORBIDDEN, content='Доступ из данной подсети запрещен')
    return await call_next(request)

app.include_router(base_api.api_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.project_host,
        port=app_settings.project_port,
        reload=True,
    )
