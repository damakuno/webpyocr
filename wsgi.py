from app.main import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.secret_key = 'uzumeorangeheart'
    app.run(host='0.0.0.0', port=port)
