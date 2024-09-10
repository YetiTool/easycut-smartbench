from kivy.app import App


def create_app(width=800, height=480):
    app = App()
    app.width = width
    app.height = height
    return app