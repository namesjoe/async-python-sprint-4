# services.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from src.models.model import URL
from src.utils.utils_funcs import generate_random_string
from src.models.model import URLAccess


async def delete_url(db: AsyncSession, short_url_id: str, user):
    async with db.begin() as conn:
        result = await conn.execute(select(URL).filter(URL.short_url_id == short_url_id))
        url = await result.scalar()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if url.deleted:
        raise HTTPException(status_code=410, detail="URL already deleted")

    if user.username != "admin" and url.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this URL")

    async with db.begin() as conn:
        await conn.commit()


async def shorten_url(db: AsyncSession, url: str, user_id: int):
    short_url_id = generate_random_string()
    new_url = URL(full_url=url, short_url_id=short_url_id, user_id=user_id)
    async with db.begin() as conn:
        await conn.add(new_url)
        await conn.commit()
    return short_url_id


async def redirect_to_original_url(db: AsyncSession, short_url_id: str, request):
    async with db.begin() as conn:
        result = await conn.execute(select(URL).filter(URL.short_url_id == short_url_id))
        url = await result.scalar()

    if not url or url.deleted:
        raise HTTPException(status_code=404, detail="URL not found")

    access_data = URLAccess(url_id=url.id, user_agent=request.headers.get("User-Agent"), client_ip=request.client.host)
    async with db.begin() as conn:
        await conn.add(access_data)
        await conn.commit()

    return url.full_url
