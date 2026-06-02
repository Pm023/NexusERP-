"""
File Upload Routes - Local + Google Drive (with detailed logging)
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from utils.storage import get_entity_folder, save_uploaded_file, MAX_FILE_SIZE
from utils.google_drive import upload_file_to_drive, check_drive_connection, list_drive_files

router = APIRouter()

@router.post("/buyer/{buyer_id}")
async def upload_buyer_doc(buyer_id: int, file: UploadFile = File(...)):
    """Upload document for buyer - Saves to local AND Google Drive"""
    try:
        contents = await file.read()
        
        if len(contents) > MAX_FILE_SIZE:
            return JSONResponse(status_code=400, content={"error": "File too large (max 50MB)"})
        
        # Save to local drive
        folder = get_entity_folder("buyer", buyer_id)
        filepath = save_uploaded_file(folder, file.filename, contents)
        
        print(f"\n[+] Local save successful: {filepath}")
        print(f"[~] Attempting Google Drive upload...")
        
        # Upload to Google Drive
        drive_result = upload_file_to_drive("buyer", buyer_id, filepath, file.filename)
        
        print(f"[~] Drive result: {drive_result}")
        
        return {
            "status": "success",
            "message": "Document uploaded to local and Google Drive",
            "file_name": file.filename,
            "local_path": filepath,
            "file_size_kb": f"{len(contents)/1024:.2f}",
            "google_drive": drive_result
        }
    
    except Exception as e:
        print(f"[!] Upload error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/manufacturer/{manufacturer_id}")
async def upload_manufacturer_doc(manufacturer_id: int, file: UploadFile = File(...)):
    """Upload document for manufacturer - Saves to local AND Google Drive"""
    try:
        contents = await file.read()
        
        if len(contents) > MAX_FILE_SIZE:
            return JSONResponse(status_code=400, content={"error": "File too large (max 50MB)"})
        
        # Save to local drive
        folder = get_entity_folder("manufacturer", manufacturer_id)
        filepath = save_uploaded_file(folder, file.filename, contents)
        
        print(f"\n[+] Local save successful: {filepath}")
        print(f"[~] Attempting Google Drive upload...")
        
        # Upload to Google Drive
        drive_result = upload_file_to_drive("manufacturer", manufacturer_id, filepath, file.filename)
        
        print(f"[~] Drive result: {drive_result}")
        
        return {
            "status": "success",
            "message": "Document uploaded to local and Google Drive",
            "file_name": file.filename,
            "local_path": filepath,
            "file_size_kb": f"{len(contents)/1024:.2f}",
            "google_drive": drive_result
        }
    
    except Exception as e:
        print(f"[!] Upload error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/direct")
async def upload_direct_doc(file: UploadFile = File(...)):
    """Upload document directly - Saves to local AND Google Drive"""
    try:
        contents = await file.read()
        
        if len(contents) > MAX_FILE_SIZE:
            return JSONResponse(status_code=400, content={"error": "File too large (max 50MB)"})
        
        # Save to local drive
        folder = get_entity_folder("direct")
        filepath = save_uploaded_file(folder, file.filename, contents)
        
        print(f"\n[+] Local save successful: {filepath}")
        print(f"[~] Attempting Google Drive upload...")
        
        # Upload to Google Drive
        drive_result = upload_file_to_drive("direct", None, filepath, file.filename)
        
        print(f"[~] Drive result: {drive_result}")
        
        return {
            "status": "success",
            "message": "Document uploaded to local and Google Drive",
            "file_name": file.filename,
            "local_path": filepath,
            "file_size_kb": f"{len(contents)/1024:.2f}",
            "google_drive": drive_result
        }
    
    except Exception as e:
        print(f"[!] Upload error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/google-drive/status")
async def get_google_drive_status():
    """Check Google Drive connection status"""
    result = check_drive_connection()
    print(f"\n[-] Drive Status Check: {result}")
    return result

@router.get("/google-drive/files/{entity_type}")
async def list_google_drive_files(entity_type: str):
    """
    List files from Google Drive
    entity_type: buyer, manufacturer, or direct
    """
    if entity_type not in ["buyer", "manufacturer", "direct"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid entity_type. Use: buyer, manufacturer, or direct"}
        )
    
    files = list_drive_files(entity_type)
    
    return {
        "status": "success",
        "entity_type": entity_type,
        "total_files": len(files),
        "files": files
    }

@router.post("/test-drive-upload")
async def test_drive_upload():
    """Test Google Drive upload with dummy data"""
    try:
        print("\n[-] Testing Google Drive upload...")
        
        # Check connection first
        status = check_drive_connection()
        print(f"Connection status: {status}")
        
        if status.get("status") != "success":
            return JSONResponse(
                status_code=500,
                content={"error": "Drive connection failed", "details": status}
            )
        
        # Try uploading test JSON
        from utils.google_drive import upload_json_to_drive
        
        test_data = {
            "test": "data",
            "timestamp": "2026-02-18",
            "message": "This is a test upload"
        }
        
        result = upload_json_to_drive("buyer", "test_upload", test_data)
        
        return {
            "status": "success",
            "message": "Test upload completed",
            "result": result
        }
    
    except Exception as e:
        print(f"[!] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})