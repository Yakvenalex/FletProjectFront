import os
from . import ft, show_snack_bar
from .utils import get_user_info, send_text_message, send_photo_message, send_file_message


class MainApp:
    def __init__(self, page: ft.Page, on_switch_to_login):
        self.page = page
        self.page.title = "Bot Interaction App"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.spacing = 20
        self.content = ft.Column(spacing=20, expand=True, alignment=ft.MainAxisAlignment.CENTER)

        # Поля для ввода данных
        self.msg_input_block = ft.TextField(label="Введите сообщение", multiline=True, min_lines=3)
        self.photo_caption = ft.TextField(label="Введите подпись к фото", multiline=True, min_lines=3)
        self.file_note = ft.TextField(label="Примечание к файлу", multiline=True, min_lines=3)

        # Выбранные файлы
        self.selected_photo = None
        self.selected_file = None

        self.on_switch_to_login = on_switch_to_login

        # Файловые выборщики для фото и файловаа
        self.photo_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.extend([self.file_picker, self.photo_picker])

    def show_login_required(self):
        # Сообщение о необходимости авторизации
        self.content.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Требуется авторизация", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
                        ft.Text("Пожалуйста, войдите в систему, чтобы получить доступ к приложению.", size=16),
                        ft.ElevatedButton(
                            "Войти",
                            icon=ft.icons.LOGIN,
                            on_click=self.on_switch_to_login
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    padding=20
                )
            )
        ]
        # Обновляем страницу для отображения изменений
        self.page.add(self.content)

    async def display(self, e=None):
        self.page.clean()
        access_token = self.page.session.get("access_token")

        if not access_token:
            self.show_login_required()
            return

        user_info = await get_user_info(access_token)
        if user_info.get("role_id") < 3:
            self.show_unauthorized(user_info)
        else:
            self.show_authorized(user_info)

    def show_exit_button(self):
        return ft.Container(
            content=ft.ElevatedButton(
                "Выйти",
                height=80,
                width=250,
                icon=ft.icons.EXIT_TO_APP,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.RED_600,
                    color=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=10),
                    elevation=5,
                ),
                on_click=self.exit_app
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    async def exit_app(self, e):
        self.page.session.clear()
        await self.on_switch_to_login(e)

    def show_unauthorized(self, user_info):
        self.content.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"Привет, {user_info.get('first_name')} {user_info.get('last_name')}!",
                                size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("К сожалению, у вас нет доступа к функционалу этого приложения.",
                                size=16, color=ft.colors.RED_400)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    padding=20,
                )
            )
        ]
        self.page.add(self.content)
        self.page.add(self.show_exit_button())

    def show_authorized(self, user_info):
        self.content.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"Добро пожаловать, {user_info.get('first_name')} {user_info.get('last_name')}!",
                                size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Выберите действие:", size=18),
                        ft.Row([
                            ft.ElevatedButton(
                                "Отправить сообщение",
                                icon=ft.icons.MESSAGE,
                                on_click=self.show_message_input
                            ),
                            ft.ElevatedButton(
                                "Отправить фото",
                                icon=ft.icons.PHOTO_CAMERA,
                                on_click=self.show_photo_input
                            ),
                            ft.ElevatedButton(
                                "Отправить файл",
                                icon=ft.icons.ATTACH_FILE,
                                on_click=self.show_file_input
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    padding=20
                )
            ),
            self.show_exit_button()
        ]
        self.page.add(self.content)

    def show_message_input(self, e):
        self.content.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Отправка сообщения боту", size=20, weight=ft.FontWeight.BOLD),
                        self.msg_input_block,
                        ft.ElevatedButton("Отправить", icon=ft.icons.SEND, on_click=self.send_message_to_bot),
                        ft.ElevatedButton("Назад", icon=ft.icons.ARROW_BACK, on_click=self.display)
                    ], spacing=20),
                    padding=20
                )
            )
        ]
        self.page.update()

    def show_photo_input(self, e):
        self.content.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Отправка фото боту", size=20, weight=ft.FontWeight.BOLD),
                        self.photo_caption,
                        ft.ElevatedButton(
                            "Выбрать фото",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: self.photo_picker.pick_files(allow_multiple=False,
                                                                            file_type=ft.FilePickerFileType.IMAGE)
                        ),
                        ft.ElevatedButton("Отправить", icon=ft.icons.SEND, on_click=self.send_photo_to_bot),
                        ft.ElevatedButton("Назад", icon=ft.icons.ARROW_BACK, on_click=self.display)
                    ], spacing=20),
                    padding=20
                )
            )
        ]
        self.page.update()

    def show_file_input(self, e):
        self.content.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Отправка файла боту", size=20, weight=ft.FontWeight.BOLD),
                        self.file_note,
                        ft.ElevatedButton(
                            "Выбрать файл",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: self.file_picker.pick_files(allow_multiple=False,
                                                                           file_type=ft.FilePickerFileType.ANY)
                        ),
                        ft.ElevatedButton("Отправить", icon=ft.icons.SEND, on_click=self.send_file_to_bot),
                        ft.ElevatedButton("Назад", icon=ft.icons.ARROW_BACK, on_click=self.display)
                    ], spacing=20),
                    padding=20
                )
            )
        ]
        self.page.update()

    async def send_message_to_bot(self, e):
        access_token = self.page.session.get("access_token")
        msg_text = self.msg_input_block.value
        await send_text_message(access_token, msg_text)
        show_snack_bar(self.page, "Сообщение успешно отправлено!")

    async def send_photo_to_bot(self, e):
        if not self.selected_photo:
            show_snack_bar(self.page, "Пожалуйста, выберите фото для отправки")
            return

        access_token = self.page.session.get("access_token")
        caption = self.photo_caption.value or 'пока без подписи'
        file_path = self.selected_photo.path

        await send_photo_message(access_token, file_path, caption)
        show_snack_bar(self.page, "Фото успешно отправлено!")

    async def send_file_to_bot(self, e):
        if not self.selected_file:
            show_snack_bar(self.page, "Пожалуйста, выберите файл для отправки")
            return

        access_token = self.page.session.get("access_token")
        note = self.file_note.value or 'Файл без примечания'
        file_path = self.selected_file.path

        await send_file_message(access_token, file_path, note)
        show_snack_bar(self.page, "Файл успешно отправлен!")

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            file_name = selected_file.name
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                self.selected_photo = selected_file
                file_type = "Фото"
            else:
                self.selected_file = selected_file
                file_type = "Файл"

            show_snack_bar(self.page, f"Выбран {file_type}: {file_name}")
        else:
            self.selected_photo = None
            self.selected_file = None
            show_snack_bar(self.page, "Медиа файл не выбран")
