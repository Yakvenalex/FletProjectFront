from app import ft, LoginForm, MainApp, RegistrationForm


async def main(page: ft.Page):
    page.title = "Одностраничное приложение"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Определение стильной тёмной темы
    dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.INDIGO_400,
            on_primary=ft.colors.WHITE,
            primary_container=ft.colors.INDIGO_700,
            on_primary_container=ft.colors.INDIGO_50,
            secondary=ft.colors.TEAL_300,
            on_secondary=ft.colors.BLACK,
            background=ft.colors.GREY_900,
            on_background=ft.colors.GREY_100,
            surface=ft.colors.GREY_900,
            on_surface=ft.colors.GREY_100,
            error=ft.colors.RED_400,
            on_error=ft.colors.WHITE,
            surface_tint=ft.colors.INDIGO_400,
            shadow=ft.colors.BLACK54,
        ),
        font_family="Inter",
        use_material3=True,
    )

    page.theme = dark_theme
    page.update()

    async def on_register_success(e):
        await login_form.display(e)

    # Объявляем экраны
    main_app = MainApp(page, on_switch_to_login=on_register_success)

    # Асинхронные коллбэки для переключения экранов
    async def on_login_success():
        await main_app.display()

    async def on_switch_to_register(e):
        await registration_form.display(e)

    login_form = LoginForm(page, on_success=on_login_success, on_switch_to_register=on_switch_to_register)
    registration_form = RegistrationForm(page, on_success=on_register_success)

    await login_form.display(e=None)  # Стартуем с формы входа


# Запускаем асинхронное приложение
ft.app(target=main)