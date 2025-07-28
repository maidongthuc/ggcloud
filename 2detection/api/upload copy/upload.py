import os

from fastapi import APIRouter
from fastapi import HTTPException, Request, UploadFile, File

router = APIRouter()



@router.post("/upload_image/")
def upload_image(
    file: UploadFile = File(...),
    request: Request = None,
    category: str = "6S", 
    index=None
):
    """
    Endpoint to upload an image and save it to static/images/raw/{type}/
    Args:
        file: Uploaded image file
        request: Request object to get base URL
        type: Category type for organizing images (default: "6S")
    Returns: URL of the uploaded image
    """
    try:
        # Check for valid image file extensions
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="File must be an image (jpg, jpeg, png, gif, bmp, webp)"
            )

        # Create directory structure: static/images/raw/{category}/
        images_dir = os.path.join("static", "images", "raw", category)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Generate filename with type and timestamp
        import time
        timestamp = int(time.time())
        if index is not None:
            new_filename = f"{category}_raw_{timestamp}_{index}{file_extension}"
        else:
            new_filename = f"{category}_raw_{timestamp}{file_extension}"

        # Save uploaded file to the organized directory
        file_path = os.path.join(images_dir, new_filename)
        with open(file_path, "wb") as buffer:
            # Sử dụng file.file.read() thay vì file.read() để tránh async
            file.file.seek(0)  # Reset file pointer to beginning
            content = file.file.read()
            buffer.write(content)

        # Construct URL to access the uploaded image
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        image_url = f"{base_url}/static/images/raw/{category}/{new_filename}"

        return {
            "url": image_url
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error upload_image: {str(e)}")

@router.post("/upload_image_dir/")
def upload_image_dir(
    file: UploadFile = File(...),
    request: Request = None,
    category: str = "6S", 
    index=None
):
    """
    Endpoint to upload an image and save it to static/images/raw/{type}/
    Args:
        file: Uploaded image file
        request: Request object to get base URL
        type: Category type for organizing images (default: "6S")
    Returns: URL of the uploaded image
    """
    try:
        # Check for valid image file extensions
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="File must be an image (jpg, jpeg, png, gif, bmp, webp)"
            )

        # Create directory structure: static/images/raw/{category}/
        images_dir = os.path.join("static", "images", "raw", category)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Generate filename with type and timestamp
        import time
        timestamp = int(time.time())
        if index is not None:
            new_filename = f"{category}_raw_{timestamp}_{index}{file_extension}"
        else:
            new_filename = f"{category}_raw_{timestamp}{file_extension}"

        # Save uploaded file to the organized directory
        file_path = os.path.join(images_dir, new_filename)
        with open(file_path, "wb") as buffer:
            # Sử dụng file.file.read() thay vì file.read() để tránh async
            file.file.seek(0)  # Reset file pointer to beginning
            content = file.file.read()
            buffer.write(content)

        # Construct URL to access the uploaded image
        image_url = f"./static/images/raw/{category}/{new_filename}"

        return {
            "url": image_url
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error upload_image: {str(e)}")

@router.post("/upload_multi_image/")
def upload_multi_image(
    files: list[UploadFile] = File(...),
    request: Request = None,
    category: str = "6S"
):
    """
    Endpoint to upload multiple images and save them to static/images/raw/{type}/
    Args:
        files: List of uploaded image files
        request: Request object to get base URL
        type: Category type for organizing images (default: "6S")
    Returns: List of URLs of the uploaded images
    """
    try:
        result = []
        for index, file in enumerate(files):
            response = upload_image(
                file=file,
                request=request,
                category=category,
                index=index
            )
            result.append(response["url"])
        return {"urls": result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading images: {str(e)}")


@router.post("/upload_multi_image_2/")
def upload_multi_image_2(
    files: list[UploadFile] = File(...),
    request: Request = None,
    category: str = "6S"
):
    """
    Endpoint to upload multiple images and save them to static/images/raw/{type}/
    Args:
        files: List of uploaded image files
        request: Request object to get base URL
        type: Category type for organizing images (default: "6S")
    Returns: List of URLs of the uploaded images
    """
    try:
        result = []
        for index, file in enumerate(files):
            response = upload_image_dir(
                file=file,
                request=request,
                category=category,
                index=index
            )
            result.append(response["url"])
        return {"urls": result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading images: {str(e)}")
