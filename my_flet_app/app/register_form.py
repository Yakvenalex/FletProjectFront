from . import show_snack_bar, ft, send_registration_data


class RegistrationForm:
    def __init__(self, page, on_success):
        self.page = page
        self.on_success = on_success
        self.name_field = ft.TextField(label="Имя", width=300)
        self.last_name_field = ft.TextField(label="Фамилия", width=300)
        self.email_field = ft.TextField(label="Email", width=300, keyboard_type=ft.KeyboardType.EMAIL)
        self.phone_number_field = ft.TextField(label="Номер телефона", width=300, keyboard_type=ft.KeyboardType.PHONE)
        self.password_field = ft.TextField(label="Пароль", width=300, password=True, can_reveal_password=True)
        self.confirm_password_field = ft.TextField(label="Повторите пароль", width=300, password=True,
                                                   can_reveal_password=True)

    def validate(self):
        if len(self.name_field.value) < 3:
            show_snack_bar(self.page, "Имя должно содержать минимум 3 символа")
            return False
        if len(self.last_name_field.value) < 3:
            show_snack_bar(self.page, "Фамилия должна содержать минимум 3 символа")
            return False
        if "@" not in self.email_field.value or "." not in self.email_field.value:
            show_snack_bar(self.page, "Введите корректный email")
            return False
        if not self.phone_number_field.value.startswith('+') or not self.phone_number_field.value[1:].isdigit():
            show_snack_bar(self.page, "Введите корректный номер телефона в формате +1234567890")
            return False
        if len(self.password_field.value) < 5:
            show_snack_bar(self.page, "Пароль должен содержать минимум 5 символов")
            return False
        if self.password_field.value != self.confirm_password_field.value:
            show_snack_bar(self.page, "Пароли не совпадают!")
            return False
        return True

    async def on_register(self, e):
        if self.validate():
            user_data = {
                "first_name": self.name_field.value,
                "last_name": self.last_name_field.value,
                "email": self.email_field.value,
                "phone_number": self.phone_number_field.value,
                "password": self.password_field.value,
                "confirm_password": self.confirm_password_field.value,
            }
            await self.process_registration(user_data)

    async def process_registration(self, user_data):
        try:
            response = await send_registration_data(user_data)
            show_snack_bar(self.page, response.get("message", "Регистрация успешно завершена!"))
            self.on_success()
        except Exception as ex:
            show_snack_bar(self.page, str(ex))


    async def display(self, e):
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    ft.Text("Регистрация", size=24, weight=ft.FontWeight.BOLD, color="#333"),
                    self.name_field,
                    self.last_name_field,
                    self.email_field,
                    self.phone_number_field,
                    self.password_field,
                    self.confirm_password_field,
                    ft.ElevatedButton(
                        text="Зарегистрироваться",
                        width=300,
                        bgcolor="#6200EE",
                        color="white",
                        on_click=self.on_register,  # Обратите внимание, что `on_register` теперь асинхронный
                    ),
                    ft.TextButton("Уже есть аккаунт? Войти", on_click=self.on_success)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )
