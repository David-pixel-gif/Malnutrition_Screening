# 🧠 Malnutrition Screening System

An AI-powered web-based solution designed to detect and predict malnutrition risk levels among children under 5 years of age, using key anthropometric indicators such as **Stunting**, **Wasting**, **Underweight**, **Overweight**, and **Under-5 Population Size**.

> ✅ Built with **FastAPI**, **React**, and **Machine Learning models trained on WHO, UNICEF & World Bank datasets.**

---

## 📸 Preview

![Landing Page](./malnutrition-detect-frontend/public/assets/hero-malnutrition.jpg)

---

## 🚀 Features

- 🔐 **User Authentication** (Signup, Login)
- 📈 **AI-based Malnutrition Prediction**
- 📥 **Batch Predictions** via Excel file upload
- 🌐 **Interactive Dashboard**
- 📊 **Global Malnutrition News Feeds**
- 🧪 **Clean ML pipeline (SVM, RandomForest, etc.)**
- 🎨 **Modern UI with Bootstrap & React Icons**
- 📁 **Clean backend structure with FastAPI + SQLAlchemy**

---

## 🧮 Tech Stack

| Frontend         | Backend        | ML / Data             | Tools & Infra            |
|------------------|----------------|------------------------|---------------------------|
| ReactJS          | FastAPI        | Scikit-Learn, Pandas   | Git, GitHub               |
| Bootstrap 5      | SQLAlchemy     | Joblib (Model Saving)  | VS Code                   |
| React-Router     | SQLite         | Pydantic, OpenCV (if needed) | Postman (API testing)   |

---

## 📂 Folder Structure


---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/David-pixel-gif/Malnutrition_Screening.git
cd Malnutrition_Screening
cd backend
python -m venv maln_venv
maln_venv\Scripts\activate   # or source maln_venv/bin/activate on Mac/Linux

pip install -r requirements.txt
uvicorn app:app --reload
cd malnutrition-detect-frontend
npm install
npm start
REACT_APP_API_BASE_URL=http://localhost:8000

📊 Sample Model Inputs
json
Copy
Edit
{
  "Stunting": 28.5,
  "Wasting": 5.6,
  "Underweight": 16.4,
  "Overweight": 3.2,
  "U5_Pop_Thousands": 545
}
🧪 Test in Postman
POST /auth/signup

POST /auth/login

POST /predict

POST /batch-predict (Upload Excel)

👨‍💻 Author
Jonathan (David-pixel-gif)
📍 Passionate about building impactful AI tools for real-world health challenges.
📫 View GitHub Profile »

📄 License
MIT License — feel free to use for educational and research purposes!

🌍 References
WHO Malnutrition Reports

UNICEF Global Databases
