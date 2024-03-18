from steroid import App

from controllers import AuthController, UserController


def main():
    app = App()

    app.addController(UserController)
    app.addController(AuthController)

    app.start()


if __name__ == "__main__":
    main()
