import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_short(
    async_client: AsyncClient,
    link_test_data: dict,
    prefix_shorten: str,
):
    # DB empty
    empty_links = await async_client.get(prefix_shorten)
    assert empty_links.status_code == status.HTTP_200_OK
    assert empty_links.json() == []

    # Добавление ссылки
    response = await async_client.post(prefix_shorten, json=link_test_data)
    assert response.status_code == status.HTTP_201_CREATED
    post_response = response.json()

    # Проверка добавленной
    links = await async_client.get(prefix_shorten)
    assert links.status_code == status.HTTP_200_OK
    get_response = response.json()

    assert get_response["original_url"] == link_test_data["full_url"]
    assert post_response["id"] == get_response["id"]

    # Получение добавленной
    link_id = get_response["id"]
    response = await async_client.get(f"{prefix_shorten}/{link_id}")
    assert response.status_code == status.HTTP_200_OK

    # Переход по ссылке
    response = await async_client.get(f"{prefix_shorten}/transfer/{link_id}")

    assert response.next_request.url == link_test_data["full_url"]
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    # Удаление
    response = await async_client.delete(f"{prefix_shorten}/{link_id}")
    assert response.status_code == status.HTTP_200_OK

    # Отсутсвие перехода
    response = await async_client.get(f"{prefix_shorten}/transfer/{link_id}")
    assert response.status_code == status.HTTP_410_GONE


@pytest.mark.asyncio
async def test_short_link_bulk(
    async_client: AsyncClient,
    link_bulk_test_data: dict,
    prefix_shorten: str,
):
    # DB empty
    empty_links = await async_client.get(prefix_shorten)
    assert empty_links.status_code == status.HTTP_200_OK
    assert empty_links.json() == []

    # add links
    response = await async_client.post(
        f"{prefix_shorten}/bulk", json=link_bulk_test_data)
    assert response.status_code == status.HTTP_201_CREATED

    # all links added
    links = await async_client.get(prefix_shorten)
    assert empty_links.status_code == status.HTTP_200_OK
    assert len(links.json()) == len(link_bulk_test_data)
