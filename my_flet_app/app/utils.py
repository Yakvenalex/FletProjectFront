import aiohttp
import flet as ft
from .config import settings

BASE_URL = settings.BASE_URL


# Вспомогательная функция для отображения SnackBar
def show_snack_bar(page, message):
    snack_bar = ft.SnackBar(content=ft.Text(message))
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()


async def send_login_request(email, password):
    url = f"{BASE_URL}/auth/login/"
    headers = {"Content-Type": "application/json"}
    payload = {"email": email, "password": password}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.text()
                raise Exception(f"Ошибка входа: {error_message}")


async def send_registration_data(data):
    url = f"{BASE_URL}/auth/register/"
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.text()
                raise Exception(f"Ошибка регистрации: {error_message}")


async def get_user_info(user_token: str):
    url = f"{BASE_URL}/auth/me/"
    headers = {
        "Cookie": f"users_access_token={user_token}",
        "accept": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def send_text_message(user_token: str, text_message: str):
    url = f"{BASE_URL}/api/send_text"
    headers = {
        "Cookie": f"users_access_token={user_token}",
        "accept": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json={"text": text_message}) as response:
            return await response.json()


async def send_photo_message(user_token: str, file_path: str, caption: str):
    url = f"{BASE_URL}/api/send_photo"
    headers = {
        "Cookie": f"users_access_token={user_token}",
        "accept": "application/json",
    }
    params = {"caption": caption}

    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            form = aiohttp.FormData()
            form.add_field(
                'file',
                file,
                filename=file_path.split('/')[-1],
                content_type='image/jpeg'
            )
            async with session.post(url, headers=headers, params=params, data=form) as response:
                return await response.json()


async def send_file_message(user_token: str, file_path: str, caption: str):
    url = f"{BASE_URL}/api/send_document"
    headers = {
        "Cookie": f"users_access_token={user_token}",
        "accept": "application/json",
    }
    params = {"caption": caption}

    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            form = aiohttp.FormData()
            form.add_field(
                'file',
                file,
                filename=file_path.split('/')[-1],
                content_type='multipart/form-data'
            )
            async with session.post(url, headers=headers, params=params, data=form) as response:
                return await response.json()
