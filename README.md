# 🚀 Flask App with Azure DevOps CI/CD

這是一個基於 **Flask** 的 Web 應用，並透過 **Azure DevOps** 進行 CI/CD 自動化部署。  
環境包含 **dev / uat / main**，並支援 PR 觸發 CI、合併後觸發 CD 部署。

---

## 📌 目錄

- [專案架構](#專案架構)
- [CI/CD 流程](#cicd-流程)
- [環境變數](#環境變數)
- [本機開發](#本機開發)
- [如何部署](#如何部署)
- [聯絡資訊](#聯絡資訊)

---

## 🏗 專案架構

```plaintext
flask_app/
│── routes/              # Flask Blueprint 路由
│── templates/           # HTML 模板
│── tests/               # 單元測試
│── requirements.txt     # 依賴管理
│── app.py               # Flask 入口文件
├── azure-pipelines.yml  # Azure DevOps Pipeline 設定
└── README.md            # 本文件
