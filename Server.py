from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime
from ultralytics import YOLO
import cv2
import shutil

app = FastAPI()

# 절대 경로 기반 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
FRAME_DIR = os.path.join(BASE_DIR, "frames")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)

# YOLO 모델 로드
try:
    model = YOLO(os.path.join(BASE_DIR, "best.pt"))
except Exception as e:
    print(f"YOLO 모델 로딩 실패: {e}")
    model = None

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # 영상 저장
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        video_path = os.path.join(UPLOAD_DIR, filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[INFO] 업로드된 파일 저장 완료: {video_path}")

        # 영상 열기 시도
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"[ERROR] 영상 파일 열기 실패: {video_path}")
            return JSONResponse(content={"status": "error", "detail": "Video file not opened"}, status_code=500)

        if model is None:
            print("[ERROR] YOLO 모델이 로드되지 않았습니다.")
            return JSONResponse(content={"status": "error", "detail": "YOLO model not loaded"}, status_code=500)

        frame_count = 0
        saved_frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            # 매 15프레임마다 YOLO 수행
            if frame_count % 15 == 0:
                results = model.predict(frame)
                if results and len(results) > 0 and hasattr(results[0], "boxes") and results[0].boxes is not None:
                    frame_name = os.path.join(FRAME_DIR, f"frame_{timestamp}_{saved_frame_count}.jpg")
                    cv2.imwrite(frame_name, frame)
                    saved_frame_count += 1

        cap.release()
        print(f"[INFO] YOLO 완료 - 총 저장된 프레임 수: {saved_frame_count}")
        return JSONResponse(content={"status": "success", "frames_saved": saved_frame_count})

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

from fastapi.staticfiles import StaticFiles

# static 폴더 서빙 추가
app.mount("/frames", StaticFiles(directory="frames"), name="frames")

@app.get("/frame_list/")
async def list_frames():
    files = os.listdir("frames")
    files.sort()  # 최신순 정렬 등 가능
    urls = [f"http://172.31.52.23:8123/frames/{name}" for name in files]
    return {"frames": urls}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8123)
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime
from ultralytics import YOLO
import cv2
import shutil

app = FastAPI()

# 절대 경로 기반 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
FRAME_DIR = os.path.join(BASE_DIR, "frames")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)

# YOLO 모델 로드
try:
    model = YOLO(os.path.join(BASE_DIR, "best.pt"))
except Exception as e:
    print(f"YOLO 모델 로딩 실패: {e}")
    model = None

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # 영상 저장
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        video_path = os.path.join(UPLOAD_DIR, filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[INFO] 업로드된 파일 저장 완료: {video_path}")

        # 영상 열기 시도
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"[ERROR] 영상 파일 열기 실패: {video_path}")
            return JSONResponse(content={"status": "error", "detail": "Video file not opened"}, status_code=500)

        if model is None:
            print("[ERROR] YOLO 모델이 로드되지 않았습니다.")
            return JSONResponse(content={"status": "error", "detail": "YOLO model not loaded"}, status_code=500)

        frame_count = 0
        saved_frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            # 매 15프레임마다 YOLO 수행
            if frame_count % 15 == 0:
                results = model.predict(frame)
                if results and len(results) > 0 and hasattr(results[0], "boxes") and results[0].boxes is not None:
                    frame_name = os.path.join(FRAME_DIR, f"frame_{timestamp}_{saved_frame_count}.jpg")
                    cv2.imwrite(frame_name, frame)
                    saved_frame_count += 1

        cap.release()
        print(f"[INFO] YOLO 완료 - 총 저장된 프레임 수: {saved_frame_count}")
        return JSONResponse(content={"status": "success", "frames_saved": saved_frame_count})

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

from fastapi.staticfiles import StaticFiles

# static 폴더 서빙 추가
app.mount("/frames", StaticFiles(directory="frames"), name="frames")

@app.get("/frame_list/")
async def list_frames():
    files = os.listdir("frames")
    files.sort()  # 최신순 정렬 등 가능
    urls = [f"http://172.31.52.23:8123/frames/{name}" for name in files]
    return {"frames": urls}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8123)
