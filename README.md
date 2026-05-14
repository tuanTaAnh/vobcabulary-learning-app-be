# 🌍 WortWander Backend

**WortWander Backend** is the API layer for an interactive German vocabulary learning application.

It powers vocabulary management, collections, starred words, flashcards, MCQ practice, learning statistics, and AI-assisted example generation.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://vobcabulary-learning-app-fe.vercel.app)

---

## 🚀 Live Demo

Frontend live demo:

https://vobcabulary-learning-app-fe.vercel.app

Frontend repository:

https://github.com/tuanTaAnh/vobcabulary-learning-app-fe

Backend repository:

https://github.com/tuanTaAnh/vobcabulary-learning-app-be

---

## 📌 Overview

**WortWander** helps German learners save vocabulary, organize words into collections, generate example sentences, practice with flashcards, answer quiz questions, and track learning progress.

This backend provides a REST API built with **FastAPI** and **SQLModel**. It stores vocabulary data, collections, study logs, quiz results, and learning statistics in a local SQLite database.

The project is designed for local development and can also be started with Docker.

---

## ✨ Key Features

### 📚 Vocabulary Management

Create, read, update, and delete German vocabulary items.

### 🗂️ Collections

Group words into collections such as:

German Vocab

Travel

Work

Food

Custom learning topics

### ⭐ Starred Words

Mark important vocabulary as starred for focused review.

### 🃏 Flashcard Support

Serve vocabulary data for German-to-meaning and meaning-to-German practice.

### ✅ MCQ Practice

Generate multiple-choice quiz questions and store correct/wrong answer logs.

### 📈 Learning Progress

Provide learning statistics such as:

Total words

Correct answers

Wrong answers

Daily activity

Study history

### 🤖 AI Example Generation

Generate example sentences for saved German words.

### 🐳 Docker-ready Setup

Run the backend locally or with Docker Compose.

---

## 🛠️ Tech Stack

Python

FastAPI

SQLModel

SQLite

Pydantic

Uvicorn

Docker

Docker Compose

---

## 📁 Project Structure

```text
.
├── app/
│   ├── main.py
│   ├── db/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── scripts/
├── docker/
├── data/
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

The exact structure may vary slightly depending on the current implementation, but the main backend logic is organized under the `app` directory.

---

## ⚙️ Environment Setup

This project uses `.env.example` as the template for environment configuration.

Real environment files are not committed to Git.

Create your local environment files from the example file:

```bash
cp .env.example .env
cp .env.example .env.docker
```

Then edit the values inside `.env` and `.env.docker` based on your local or Docker setup.

Example environment variables:

```env
DATABASE_URL=sqlite:///./data/vocab.db
OPENAI_API_KEY=your_api_key_here
```

Use `.env` for local development.

Use `.env.docker` for Docker-based execution.

---

## 💻 Local Development

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

The backend should be available at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

## 🐳 Docker Usage

Build and run the backend with Docker Compose:

```bash
docker compose up -d --build backend
```

Stop the service:

```bash
docker compose down
```

View backend logs:

```bash
docker compose logs -f backend
```

---

## 🗄️ Database

The default setup uses SQLite for simplicity.

A typical local database path is:

```text
data/vocab.db
```

Make sure the `data` directory exists if your environment uses a local SQLite file.

Example:

```bash
mkdir -p data
```

---

## 📥 Importing Vocabulary Data

If the project includes an Excel ingestion script, vocabulary data can be imported with:

```bash
python app/scripts/ingest_excel_vocab.py
```

The script can be configured to read from a predefined Excel file and insert vocabulary into the local database.

---

## 🔌 Main API Capabilities

The backend supports APIs for:

Collections

Vocabulary

Starred words

Generated examples

Study logs

Learning statistics

Flashcard practice

MCQ practice

AI scene/chat practice

The frontend consumes these APIs to provide the full WortWander learning experience.

---

## 🖥️ Frontend Integration

This backend is designed to work with the WortWander frontend:

```text
https://github.com/tuanTaAnh/vobcabulary-learning-app-fe
```

When running locally, make sure the frontend points to the correct backend URL.

Example frontend environment variable:

```env
VITE_API_BASE=http://localhost:8000
```

Then start the frontend from the frontend repository:

```bash
npm run dev
```

Open the frontend in your browser:

```text
http://localhost:5173
```

---

## 🔄 Recommended Development Workflow

Start the backend:

```bash
uvicorn app.main:app --reload
```

Start the frontend:

```bash
npm run dev
```

Open the app:

```text
http://localhost:5173
```

Open backend API documentation:

```text
http://localhost:8000/docs
```

---

## 🔐 GitHub Notes

Do not commit real environment files.

The following files should normally stay local:

```text
.env
.env.docker
data/*.db
__pycache__/
.venv/
```

Only commit the environment template:

```text
.env.example
```

This allows other developers to create their own `.env` and `.env.docker` files safely.

---

## 📎 Related Repository

Frontend repository:

https://github.com/tuanTaAnh/vobcabulary-learning-app-fe

Live demo:

https://vobcabulary-learning-app-fe.vercel.app

---

## 👨‍💻 Author

Developed by **Tuan Ta Anh**

GitHub:

https://github.com/tuanTaAnh
