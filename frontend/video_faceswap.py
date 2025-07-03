import streamlit as st
import time
import requests
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("MAXSTUDIO_API_KEY")

# ----------------------------
# MaxStudio API Helper Methods
# ----------------------------

def detect_faces(video_url, api_key):
    url = "https://api.maxstudio.ai/detect-face-video"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    payload = {"videoUrl": video_url}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Face detection failed: {e}")
        return None

def video_face_swap(api_key, media_url, swap_id, original_face_url, new_face_url):
    url = "https://api.maxstudio.ai/video-swap"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    payload = {
        "mediaUrl": media_url,
        "faces": [
            {
                "originalFace": original_face_url,
                "newFace": new_face_url
            }
        ],
        "swapId": swap_id
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Swap request failed: {e}")
        return None

def check_job_status(job_id, api_key):
    url = f"https://api.maxstudio.ai/video-swap/{job_id}"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Failed to check job status: {e}")
        return None

# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="🎬 Video Face Swap", layout="centered")
st.title("🎬 Face Swap on Video using MaxStudio API")
st.markdown("""
Upload a **public video URL** and a **public face image URL**.  
We'll perform face detection and initiate a face swap using MaxStudio API.
""")
st.info("🔒 Make sure both URLs are publicly accessible (Google Drive direct links won't work unless shared properly).")

# Inputs
video_url = st.text_input("🎞️ Enter your public video URL")
new_face_url = st.text_input("🧑 Enter your new face image URL")

if st.button("🚀 Start Face Swap"):
    if not video_url or not new_face_url:
        st.warning("⚠️ Both video and face image URLs are required.")
    elif not API_KEY:
        st.error("❌ Missing API key! Please set `MAXSTUDIO_API_KEY` in your .env file.")
    else:
        with st.spinner("🔍 Detecting face in video..."):
            detect_result = detect_faces(video_url, API_KEY)

        if detect_result:
            swap_id = detect_result.get("swapId")
            detected_faces = detect_result.get("detectedFaces", [])

            if not detected_faces:
                st.error("❌ No face detected in the video.")
            else:
                original_face_url = detected_faces[0]
                st.success(f"✅ Face detected at: {original_face_url}")

                with st.spinner("🧠 Sending face swap request..."):
                    swap_result = video_face_swap(API_KEY, video_url, swap_id, original_face_url, new_face_url)

                if swap_result:
                    job_id = swap_result.get("jobId")
                    st.success(f"🛠️ Swap job started (Job ID: `{job_id}`)")
                    status_placeholder = st.empty()

                    # Poll every 5 seconds, max ~6 mins
                    for attempt in range(72):
                        time.sleep(5)
                        job_status = check_job_status(job_id, API_KEY)

                        if not job_status:
                            break

                        status = job_status.get("status", "unknown")
                        status_placeholder.info(f"🔄 Status: {status}")

                        if status == "completed":
                            result = job_status.get("result", {})
                            st.success("🎉 Face Swap Completed!")
                            st.video(result.get("previewUrl"))
                            st.markdown(f"[📥 Download Final Video]({result.get('mediaUrl')})", unsafe_allow_html=True)
                            break
                        elif status in ["failed", "not-found"]:
                            st.error("❌ Job failed or was not found.")
                            break
                    else:
                        st.warning("⏰ Timed out after 6 minutes. Please check job status manually.")
                else:
                    st.error("❌ Failed to initiate face swap.")
