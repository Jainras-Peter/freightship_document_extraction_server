from fastapi import UploadFile, HTTPException

def validate_file(file: UploadFile):
    if file.content_type == "application/pdf":
        return "pdf"
    elif file.content_type.startswith("image/"):
        return "image"
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and Images are supported.")
