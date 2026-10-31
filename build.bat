@echo off
call .venv\Scripts\activate.bat
pyinstaller --noconfirm --clean --onefile --console ^
    --name "telegram-cli" ^
    --add-data ".env;." ^
    --collect-all "pyrogram" ^
    --collect-all "tgcrypto" ^
    main.py
pause