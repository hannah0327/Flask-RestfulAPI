# Flask-RESTful API 專案

---

## 專案簡介

這是一個使用 Flask 和 Flask-RESTful 建立的 RESTful API 專案，提供書籍資訊的管理功能以及使用者認證。專案整合了 SQLAlchemy 進行資料庫操作、JWT 實現權限驗證，並透過 Flask-APISpec 產生 Swagger (OpenAPI) 文件。

## 專案功能

* **使用者認證**：提供登入功能，成功登入後會回傳 JWT Token，用於後續需要權限的 API 請求。
* **書籍管理**：
    * 取得所有書籍清單。
    * 依據 ID 取得特定書籍資訊。
    * 新增書籍（需登入驗證）。
    * 更新書籍資訊（需登入驗證）。
* **API 文件**：自動產生 Swagger UI 介面，方便開發者查閱和測試 API。

---

## 核心檔案說明
| 檔案/資料夾                       | 說明                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `main.py`                    | 應用程式的入口點，初始化 Flask 應用並啟動伺服器。                                                                                          |
| `resources/__init__.py`      | 設定 Flask 應用、初始化 API 物件、資料庫連線與 Swagger 文件，並匯入各個資源模組。                                                                   |
| `models/book_model.py`       | 定義 `BookModel` 的 SQLAlchemy 模型，對應資料庫中的 `books` 表。                                                                     |
| `models/user_model.py`       | 定義 `UserModel` 的 SQLAlchemy 模型，對應資料庫中的 `users` 表。                                                                     |
| `api_tools.py`               | 包含 `token_required` 裝飾器，用於驗證 JWT Token，保護需要授權的 API。                                                                   |
| `resources/book_resource.py` | 定義 `BookResource` 和 `BookListResource`，處理書籍相關的 API 請求；結合 Marshmallow schema 處理驗證與序列化，並透過 Flask-APISpec 生成 Swagger 文件。 |
| `resources/user_resource.py` | 定義 `LoginResource`，處理使用者登入並回傳 JWT Token。                                                                              |
| `services/book_service.py`   | 實作書籍相關的商業邏輯（如新增、查詢、更新書籍等）。                                                                                            |
| `services/user_service.py`   | 實作使用者相關的商業邏輯（如驗證登入帳密）。                                                                                                |
| `common/constants.py`        | 儲存專案用到的常數值，如 JWT 加密密鑰 `LOGIN_SECRET`。                                                                                 |
| `requirements.txt`           | 列出專案所需安裝的所有 Python 套件與對應版本。                                                                                           |

---

## 安裝與執行
### 1. 克隆專案

```bash
git clone <你的專案URL>
cd <你的專案資料夾>
```

### 2. 建立虛擬環境與安裝依賴
建議使用 pipenv 或 venv 建立虛擬環境，以隔離專案依賴。
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt # 你需要手動建立一個 requirements.txt 文件
```

### 3. 資料庫設定與連線
本專案使用 MySQL 資料庫。請確保您已安裝 MySQL 並建立了資料庫。
在 resources/__init__.py 中修改以下設定：
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<帳號>:<密碼>@<主機>/<資料庫名稱>'
```

### 4. 設定 JWT 密鑰 (可選)
在 common/constants.py 中，設定你的 LOGIN_SECRET。這是一個用於 JWT 加密的密鑰，請確保其安全性。
```bash
LOGIN_SECRET = "your_super_secret_key" # 請替換成一個複雜且安全的密鑰
```

### 5. 啟動專案
```bash
python main.py
```
伺服器將在 [http://localhost:5000](http://127.0.0.1:5000) 執行。

---

## 📘 API 文件與 Swagger UI
啟動伺服器後，可透過以下路徑查看 API 文件：
- Swagger UI: http://localhost:5000/swagger-ui/
 <img width="938" height="428" alt="image" src="https://github.com/user-attachments/assets/94862bdc-330d-4c53-8a6a-cd223abaaa0b" />

- Swagger YAML: http://localhost:5000/swagger.yaml

---

## 🔐 JWT 驗證機制
用戶登入後會獲得一組 JWT Token，部分 API（新增/修改書籍）需此 Token 驗證，請在 HTTP Header 中加入：
```bash
token: <your-jwt-token>
```

---

## 📚 API 路由說明
### 📘 書籍 Book APIs
| Method | Path          | 說明          |
| ------ | ------------- | ----------- |
| GET    | `/books`      | 查詢所有書籍      |
| GET    | `/books/<id>` | 查詢指定書籍      |
| POST   | `/books`      | 新增書籍（需 JWT） |
| PUT    | `/books/<id>` | 更新書籍（需 JWT） |

- 傳入欄位（POST/PUT）：
{
  "name": "Book Title",
  "author": "Author Name",
  "publish_time": "2024-01-01T12:00:00"
}


### 👤 使用者 Login API
| Method | Path     | 說明                  |
| ------ | -------- | ------------------- |
| POST   | `/login` | 用戶登入，成功回傳 JWT Token |

- 登入請求：
{
  "username": "test_user",
  "password": "123456"
}

- 回應格式：
{
  "id": 1,
  "username": "test_user",
  "token": "<JWT token>"
}

---

## 🛡️注意事項
- 請確保 MySQL 資料庫已建立並啟用。

- LOGIN_SECRET 為 JWT 加密密鑰，建議於 common/constants.py 中妥善設定為隨機字串。

- Swagger UI 自動讀取 @doc、@marshal_with 等裝飾器資訊產生介面說明。
