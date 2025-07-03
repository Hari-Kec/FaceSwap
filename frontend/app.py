# app.py
import streamlit as st
from PIL import Image
import tempfile
from utils import call_faceswap_api
import time
import uuid
import requests
from dotenv import load_dotenv
import os

# Load environment variables
# load_dotenv()
# api_key = os.getenv("MAXSTUDIO_API_KEY")

# # ---------------------------- Utility Functions ----------------------------
# def detect_faces(video_url, api_key):
#     url = "https://api.maxstudio.ai/detect-face-video"
#     headers = {"Content-Type": "application/json", "x-api-key": api_key}
#     payload = {"videoUrl": video_url}
#     try:
#         res = requests.post(url, headers=headers, json=payload)
#         res.raise_for_status()
#         return res.json()
#     except Exception as e:
#         st.error(f"❌ Face detection failed: {str(e)}")
#         return None

# def video_face_swap(api_key, media_url, swap_id, original_face_url, new_face_url):
#     url = "https://api.maxstudio.ai/video-swap"
#     headers = {"Content-Type": "application/json", "x-api-key": api_key}
#     payload = {
#         "mediaUrl": media_url,
#         "faces": [{"originalFace": original_face_url, "newFace": new_face_url}],
#         "swapId": swap_id,
#     }
#     try:
#         res = requests.post(url, headers=headers, json=payload)
#         res.raise_for_status()
#         return res.json()
#     except Exception as e:
#         st.error(f"❌ Face swap request failed: {str(e)}")
#         return None

# def check_job_status(job_id, api_key):
#     url = f"https://api.maxstudio.ai/video-swap/{job_id}"
#     headers = {"x-api-key": api_key}
#     try:
#         res = requests.get(url, headers=headers)
#         res.raise_for_status()
#         return res.json()
#     except Exception as e:
#         st.error(f"❌ Job status check failed: {str(e)}")
#         return None

# ---------------------------- Streamlit UI ----------------------------
st.set_page_config(
    page_title="🎭 FaceSwap AI",
    page_icon="🧠",
    layout="centered"
)

st.title("FaceSwap AI App")
st.caption("Swap faces on images and videos using advanced AI")

st.markdown("### 📸 Face Swap on Images")
st.markdown("Upload a **source face image** and a **target image** (like a poster or selfie).")

# Image upload columns
col1, col2 = st.columns(2)
with col1:
    source_face = st.file_uploader("Upload Source Face", type=["jpg", "jpeg", "png"], key="src")
    if source_face:
        st.image(source_face, caption="👤 Source Face", use_column_width=True)

with col2:
    target_img = st.file_uploader("Upload Target Image", type=["jpg", "jpeg", "png"], key="tgt")
    if target_img:
        st.image(target_img, caption="🎯 Target Image", use_column_width=True)

if st.button("🔁 Swap Faces") and source_face and target_img:
    with st.spinner("🔄 Swapping faces, please wait..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_src, \
                 tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_tgt:
                tmp_src.write(source_face.read())
                tmp_tgt.write(target_img.read())
                tmp_src.flush()
                tmp_tgt.flush()
                result_img_bytes = call_faceswap_api(tmp_src.name, tmp_tgt.name)
        except Exception as e:
            st.error(f"⚠️ Unexpected error during face swap: {str(e)}")
            result_img_bytes = None

        if result_img_bytes:
            st.success("✅ Face swap successful!")
            st.image(result_img_bytes, caption="🖼️ Swapped Output", use_container_width=True)
        else:
            st.error("❌ Face swap failed. Try different images.")

st.markdown("---")
# st.markdown("### 🎬 Face Swap on Video (via MaxStudio API)")
# st.info("Note: Your video and face image URLs must be **publicly accessible**.")

# video_url = st.text_input("🎞️ Enter your public video URL")
# new_face_url = st.text_input("🧑 Enter your new face image URL")

# if st.button("🚀 Start Face Swap"):
#     if not video_url or not new_face_url:
#         st.warning("⚠️ Both video and face image URLs are required.")
#     else:
#         with st.spinner("🔍 Detecting face in video..."):
#             detect_result = detect_faces(video_url, api_key)

#         if detect_result:
#             swap_id = detect_result.get("swapId")
#             detected_faces = detect_result.get("detectedFaces", [])

#             if not detected_faces:
#                 st.error("❌ No face detected in the video.")
#             else:
#                 original_face_url = detected_faces[0]
#                 st.success(f"✅ Face detected at: {original_face_url}")

#                 with st.spinner("🧠 Sending face swap request..."):
#                     swap_result = video_face_swap(api_key, video_url, swap_id, original_face_url, new_face_url)

#                 if swap_result:
#                     job_id = swap_result.get("jobId")
#                     st.success(f"🛠️ Swap job started (Job ID: `{job_id}`)")
#                     status_placeholder = st.empty()
#                     poll_attempts = 72

#                     for _ in range(poll_attempts):
#                         time.sleep(5)
#                         job_status = check_job_status(job_id, api_key)

#                         if not job_status:
#                             break

#                         status = job_status.get("status", "unknown")
#                         status_placeholder.info(f"🔄 Status: {status}")

#                         if status == "completed":
#                             result = job_status.get("result", {})
#                             st.success("🎉 Swap completed!")
#                             st.video(result.get("previewUrl"))
#                             st.markdown(
#                                 f"[📥 Download Final Video]({result.get('mediaUrl')})",
#                                 unsafe_allow_html=True
#                             )
#                             break
#                         elif status in ["failed", "not-found"]:
#                             st.error("❌ The job failed or was not found.")
#                             break
#                     else:
#                         st.warning("⏰ Timed out after 6 minutes. Please check job status manually.")
#                 else:
#                     st.error("❌ Face swap job could not be created.")

