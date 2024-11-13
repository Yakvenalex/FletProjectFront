from . import show_snack_bar, ft, send_login_request


class LoginForm:
    def __init__(self, page, on_success, on_switch_to_register):
        self.page = page
        self.on_success = on_success
        self.on_switch_to_register = on_switch_to_register
        self.email_field = ft.TextField(
            label="Email",
            width=300,
            keyboard_type=ft.KeyboardType.EMAIL,
            value='user@example.com',
        )
        self.password_field = ft.TextField(
            label="Пароль",
            width=300,
            password=True,
            can_reveal_password=True,
            value='string'
        )

    async def on_login(self, e):
        if not self.email_field.value or not self.password_field.value:
            show_snack_bar(self.page, "Заполните все поля для входа")
            return

        await self.process_login(self.email_field.value, self.password_field.value)

    async def process_login(self, email, password):
        try:
            response = await send_login_request(email, password)
            if response.get("ok"):
                access_token = response.get("access_token")

                if access_token:
                    self.page.session.set("access_token", access_token)
                    show_snack_bar(self.page, response.get("message", "Вход успешно выполнен!"))
                    self.clear_fields()
                    await self.on_success()
                else:
                    show_snack_bar(self.page, "Токен доступа не получен.")
            else:
                show_snack_bar(self.page, response.get("message", "Ошибка авторизации."))
        except Exception as ex:
            show_snack_bar(self.page, str(ex))

    def clear_fields(self):
        self.email_field.value = ""
        self.password_field.value = ""
        self.page.update()

    async def display(self, e):
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Вход", size=24, weight=ft.FontWeight.BOLD, color="#333"),
                    self.email_field,
                    self.password_field,
                    ft.ElevatedButton(
                        text="Войти",
                        width=300,
                        bgcolor="#6200EE",
                        color="white",
                        on_click=self.on_login,  # Назначаем асинхронный метод напрямую
                    ),
                    ft.TextButton(
                        "Нет аккаунта? Зарегистрироваться",
                        on_click=self.on_switch_to_register
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )
