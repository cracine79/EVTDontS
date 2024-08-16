from main import create_app
from config import DevConfig

print("hello")
if __name__=='__main__':
    app=create_app(DevConfig)
    app.run(host="0.0.0.0", port=3000)