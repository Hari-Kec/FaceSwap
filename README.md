

# 🧠 FaceSwap AI App

Swap faces between two images — or replace faces in **videos** using powerful AI.  
Built with FastAPI backend, Streamlit frontend, and optional video face swap via MaxStudio API.

---

## 🚀 Features

- 🔁 **Image Face Swap** using local ONNX models (`insightface`)
- 🎬 **Video Face Swap** powered by MaxStudio AI
- 🧠 FastAPI backend with file upload & face swap logic
- ⚡ Streamlit frontend for seamless interaction
- 🔐 Secure API key-based integration (MaxStudio)
- 🖼️ Real-time image preview and video rendering

---

## 🏗️ Project Structure

```

FaceSwap/
│
├── backend/
│   ├── main.py              # FastAPI server
│   ├── face\_swapper.py      # Core face swapping logic using InsightFace
│   ├── utils.py             # File I/O helpers
│
├── frontend/
│   ├── app.py               # Streamlit UI app
│   └── utils.py             # Calls backend face swap API
│
├── models/                  # Pre-downloaded ONNX models
│   ├── inswapper\_128.onnx
│   └── buffalo\_l/
│       ├── detection\_10g.onnx
│       ├── recognition.onnx
│       ├── genderage.onnx
│       ├── 2d106det.onnx
│       └── 1k3d68.onnx
│
├── static/output/           # Swapped image results
├── requirements.txt
└── README.md

````

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Hari-Kec/FaceSwap.git
cd FaceSwap
````

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt #for every folder(backend , frontend)
```

Ensure you’ve installed:

* Python ≥ 3.9
* Visual C++ Build Tools (for InsightFace)

---

## 📦 Download ONNX Models

* Place `inswapper_128.onnx` inside `models/`
* Create `models/buffalo_l/` and place these:

```text
- detection_10g.onnx
- recognition.onnx
- genderage.onnx
- 2d106det.onnx
- 1k3d68.onnx
```

⚠️ Make sure filenames match **exactly**, else InsightFace will redownload models.

---

## 🚀 Run the App

### 1. Start FastAPI backend

```bash
cd backend
uvicorn main:app --reload
```

The backend will run at: `http://localhost:8000`

### 2. Start Streamlit frontend

```bash
cd ../frontend
streamlit run app.py
```

---

## 🔐 Configure MaxStudio API (Video Swap)

1. Get your MaxStudio API key: [https://api.maxstudio.ai](https://api.maxstudio.ai)
2. Add it to `.env` or set it inline:

```python
MAXSTUDIO_API_KEY = "your_key_here"
```

3. Paste **public URLs** of:

   * Target video
   * Face image

Streamlit UI will handle:

* Face detection
* Swap request
* Progress polling
* Preview + download

---

## 📸 Demo

https://drive.google.com/file/d/1ufDAHqFsD01S1WfNzv2LVvBV_f6wpnWW/view?usp=sharing
---

## 🧠 Tech Stack

| Layer     | Tech                          |
| --------- | ----------------------------- |
| Frontend  | Streamlit                     |
| Backend   | FastAPI                       |
| AI Models | InsightFace (ONNX), MaxStudio |
| Auth/API  | API Key (for MaxStudio)       |
| Extras    | Tempfile, UUID, Requests      |

---


## 📄 License

MIT License

---

## 📬 Contact

Feel free to open issues or suggestions!

