---
title: WortWander Backend
emoji: 📚
colorFrom: yellow
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# WortWander Backend

Backend API for **WortWander**, a German vocabulary learning app.

This Space runs the FastAPI backend for vocabulary management, collections, flashcards, MCQ practice, study logs, and learning progress.

## API

After deployment, the backend will be available at:

```text
https://anhtuan19981998-wortwander-backend.hf.space
```

Useful endpoints:

```text
/docs
/vocabs
/collections
/stats
```

Example:

```text
https://anhtuan19981998-wortwander-backend.hf.space/docs
```

## Frontend Repository

The frontend is deployed separately.

```text
https://github.com/tuanTaAnh/vobcabulary-learning-app-fe
```

## Backend Repository

```text
https://github.com/tuanTaAnh/vobcabulary-learning-app-be
```

## Notes

This project does not push the local SQLite database file `data/vocab.db` to Hugging Face.

Instead, vocabulary seed data is stored as:

```text
data/vocab_seed.json
```

Environment files are not pushed directly. Use:

```text
.env.example
```

to create your own `.env` or `.env.docker` file locally.