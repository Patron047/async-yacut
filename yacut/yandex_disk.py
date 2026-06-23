import asyncio
import os
import urllib.parse

import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DISK_TOKEN = os.environ.get('DISK_TOKEN')

AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def upload_file_to_disk(session, file_storage):
    """Асинхронно загружает один файл на Яндекс Диск."""
    filename = file_storage.filename
    path = f'app:/{filename}'
    upload_url_params = {
        'path': path,
        'overwrite': 'true'
    }
    async with session.get(
        f'{API_HOST}{API_VERSION}/disk/resources/upload',
        params=upload_url_params,
        headers=AUTH_HEADERS
    ) as response:
        data = await response.json()
        upload_href = data['href']

    file_data = file_storage.read()
    async with session.put(upload_href, data=file_data) as response:
        location = response.headers.get('Location')
        if not location:
            raise Exception(f'Не получен заголовок для файла {filename}')
        disk_path = urllib.parse.unquote(location).replace('/disk', '')
    download_params = {'path': disk_path}
    async with session.get(
        f'{API_HOST}{API_VERSION}/disk/resources/download',
        params=download_params,
        headers=AUTH_HEADERS
    ) as response:
        download_data = await response.json()
        download_link = download_data['href']

    return {
        'filename': filename,
        'disk_path': disk_path,
        'download_link': download_link
    }


async def upload_files_to_disk(files_storage_list):
    """Загружает список файлов на Яндекс Диск асинхронно."""
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            upload_file_to_disk(session, file_storage)
            for file_storage in files_storage_list
        ]
        results = await asyncio.gather(*tasks)
    return results
