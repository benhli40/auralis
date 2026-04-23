from app import FuturePlayerApp


def main() -> int:
    app = FuturePlayerApp()
    try:
        return app.run()
    finally:
        app.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())