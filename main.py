from fastapi import FastAPI, UploadFile, File, HTTPException
import psutil
import subprocess
import os

app = FastAPI(title="Device Farm Backend System")

def get_apk_package_name(apk_path: str) -> str:
    try:
        output = subprocess.check_output(
            ["aapt", "dump", "badging", apk_path],
            text=True
        )
        for line in output.splitlines():
            if line.startswith("package:"):
                return line.split("name='")[1].split("'")[0]
    except Exception:
        return ""


#function for check server status
@app.get("/health")
def health():
    return {
        "status": "OK",
        "message": "This works fine!"
    }

#function for server healthcheck
@app.get("/metrics")
def metrics():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent
    }

#function for get devices list
@app.get("/devices")
def devices():
    try:
        result = subprocess.check_output(
            ["adb", "devices"],
            stderr=subprocess.STDOUT,
            text=True
        )

        lines = result.strip().split("\n")[1:]
        devices = []

        for line in lines:
            if line.strip():
                device_id, status = line.split("\t")
                devices.append({
                    "id": device_id,
                    "status": status
                })

        return {"devices": devices}

    except Exception as e:
        return {"error": str(e)}

#function for uploading APK
@app.post("/upload-apk")
async def upload_apk(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    if not file.filename.lower().endswith(".apk"):
        raise HTTPException(
            status_code=400,
            detail="Only .apk files are allowed"
        )

    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": file_path
    }
'''@app.post("/upload-apk")
async def upload_apk(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": file_path
    }
    '''

#function for install apk
@app.post("/install-apk")
def install_apk(device_id: str, apk_path: str):
    if not os.path.exists(apk_path):
        return {"status": "failed", "error": "APK not found"}

    package_name = get_apk_package_name(apk_path)
    if not package_name:
        return {"status": "failed", "error": "Unable to read package name"}

    try:
        # Check if installed
        installed = subprocess.check_output(
            ["adb", "-s", device_id, "shell", "pm", "list", "packages", package_name],
            text=True
        )

        if package_name in installed:
            subprocess.check_output(
                ["adb", "-s", device_id, "uninstall", package_name],
                text=True
            )

        # Install fresh APK
        result = subprocess.check_output(
            ["adb", "-s", device_id, "install", apk_path],
            stderr=subprocess.STDOUT,
            text=True
        )

        return {
            "status": "success",
            "device": device_id,
            "package": package_name,
            "output": result
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "device": device_id,
            "error": e.output
        }
