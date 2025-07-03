import requests

def call_faceswap_api(source_img_path, target_img_path, backend_url="https://faceswap-l102.onrender.com"):
    with open(source_img_path, "rb") as src, open(target_img_path, "rb") as tgt:
        files = {
            "source_face": src,
            "target_image": tgt
        }
        response = requests.post(backend_url, files=files)

    if response.status_code == 200:
        return response.content 
    else:
        try:
            error_msg = response.json()
        except Exception:
            error_msg = response.text 
        print("❌ FaceSwap API error:", response.status_code, error_msg)
        return None
