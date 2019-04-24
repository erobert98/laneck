import os
from laneck import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5432))
    app.run(host= '0.0.0.0', port = port) 
