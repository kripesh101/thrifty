def init_app():
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from utils.prod import prod

    app = FastAPI()

    origins = ["http://*"]
    regex = "http://.*"

    if (prod):
        origins = [
            "https://thrifty.pages.dev",
            "https://*.thrifty.pages.dev"
        ]
        regex = "https://.*\.thrifty\.pages\.dev"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_origin_regex=regex,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
