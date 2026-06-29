from src.app import create_app
from src.config.app_config import APP_CONFIG

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(APP_CONFIG.PORT), log_config=None)
