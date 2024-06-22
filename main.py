from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import os
import shutil
import json
from pathlib import Path

app = FastAPI()

# Directory for storing uploaded images and generated icons
UPLOAD_DIRECTORY = "uploads"
OUTPUT_DIRECTORY = "output_icons"

# JSON content for AppIcon.appiconset
json_content = {
    "images": [
        {"size":"60x60","expected-size":"180","filename":"180.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"3x"},
        {"size":"40x40","expected-size":"80","filename":"80.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"2x"},
        {"size":"40x40","expected-size":"120","filename":"120.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"3x"},
        {"size":"60x60","expected-size":"120","filename":"120.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"2x"},
        {"size":"57x57","expected-size":"57","filename":"57.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"1x"},
        {"size":"29x29","expected-size":"58","filename":"58.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"2x"},
        {"size":"29x29","expected-size":"29","filename":"29.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"1x"},
        {"size":"29x29","expected-size":"87","filename":"87.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"3x"},
        {"size":"57x57","expected-size":"114","filename":"114.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"2x"},
        {"size":"20x20","expected-size":"40","filename":"40.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"2x"},
        {"size":"20x20","expected-size":"60","filename":"60.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"iphone","scale":"3x"},
        {"size":"1024x1024","expected-size":"1024","filename":"1024.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ios-marketing","scale":"1x"},
        {"size":"40x40","expected-size":"80","filename":"80.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"2x"},
        {"size":"72x72","expected-size":"72","filename":"72.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"1x"},
        {"size":"76x76","expected-size":"152","filename":"152.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"2x"},
        {"size":"50x50","expected-size":"100","filename":"100.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"2x"},
        {"size":"29x29","expected-size":"58","filename":"58.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"2x"},
        {"size":"76x76","expected-size":"76","filename":"76.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"1x"},
        {"size":"29x29","expected-size":"29","filename":"29.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"1x"},
        {"size":"50x50","expected-size":"50","filename":"50.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"1x"},
        {"size":"72x72","expected-size":"144","filename":"144.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"2x"},
        {"size":"40x40","expected-size":"40","filename":"40.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"1x"},
        {"size":"83.5x83.5","expected-size":"167","filename":"167.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"2x"},
        {"size":"20x20","expected-size":"20","filename":"20.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"1x"},
        {"size":"20x20","expected-size":"40","filename":"40.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"ipad","scale":"2x"},
        {"idiom":"watch","filename":"172.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"38mm","scale":"2x","size":"86x86","expected-size":"172","role":"quickLook"},
        {"idiom":"watch","filename":"80.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"38mm","scale":"2x","size":"40x40","expected-size":"80","role":"appLauncher"},
        {"idiom":"watch","filename":"88.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"40mm","scale":"2x","size":"44x44","expected-size":"88","role":"appLauncher"},
        {"idiom":"watch","filename":"102.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"41mm","scale":"2x","size":"45x45","expected-size":"102","role":"appLauncher"},
        {"idiom":"watch","filename":"92.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"41mm","scale":"2x","size":"46x46","expected-size":"92","role":"appLauncher"},
        {"idiom":"watch","filename":"100.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"44mm","scale":"2x","size":"50x50","expected-size":"100","role":"appLauncher"},
        {"idiom":"watch","filename":"196.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"42mm","scale":"2x","size":"98x98","expected-size":"196","role":"quickLook"},
        {"idiom":"watch","filename":"216.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"44mm","scale":"2x","size":"108x108","expected-size":"216","role":"quickLook"},
        {"idiom":"watch","filename":"48.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"38mm","scale":"2x","size":"24x24","expected-size":"48","role":"notificationCenter"},
        {"idiom":"watch","filename":"55.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"42mm","scale":"2x","size":"27.5x27.5","expected-size":"55","role":"notificationCenter"},
        {"idiom":"watch","filename":"66.png","folder":"Assets.xcassets/AppIcon.appiconset/","subtype":"45mm","scale":"2x","size":"33x33","expected-size":"66","role":"notificationCenter"},
        {"size":"29x29","expected-size":"87","filename":"87.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"watch","role":"companionSettings","scale":"3x"},
        {"size":"29x29","expected-size":"58","filename":"58.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"watch","role":"companionSettings","scale":"2x"},
        {"size":"1024x1024","expected-size":"1024","filename":"1024.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"watch-marketing","scale":"1x"},
        {"size":"128x128","expected-size":"128","filename":"128.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"1x"},
        {"size":"256x256","expected-size":"256","filename":"256.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"1x"},
        {"size":"128x128","expected-size":"256","filename":"256.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"2x"},
        {"size":"256x256","expected-size":"512","filename":"512.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"2x"},
        {"size":"32x32","expected-size":"32","filename":"32.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"1x"},
        {"size":"512x512","expected-size":"512","filename":"512.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"1x"},
        {"size":"16x16","expected-size":"16","filename":"16.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"1x"},
        {"size":"16x16","expected-size":"32","filename":"32.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"2x"},
        {"size":"32x32","expected-size":"64","filename":"64.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"2x"},
        {"size":"512x512","expected-size":"1024","filename":"1024.png","folder":"Assets.xcassets/AppIcon.appiconset/","idiom":"mac","scale":"2x"}
    ]
}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Create directories if they don't exist
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    # Save the uploaded file
    upload_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process the uploaded image
    process_image(upload_path, OUTPUT_DIRECTORY)

    # Return the output directory as a downloadable zip file
    zip_path = shutil.make_archive("AppIcons", 'zip', OUTPUT_DIRECTORY)
    return FileResponse(zip_path, filename="AppIcons.zip")

def process_image(input_path: str, output_directory: str):
    # Open the original icon
    try:
        original_icon = Image.open(input_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        raise

    # Create directories for ios
    ios_dir = os.path.join(output_directory, "Assets.xcassets")
    appiconset_dir = os.path.join(ios_dir, "AppIcon.appiconset")

    if not os.path.exists(appiconset_dir):
        os.makedirs(appiconset_dir)

    # Create directories for android
    android_dirs = {
        "mipmap-hdpi": (72, 72),
        "mipmap-mdpi": (48, 48),
        "mipmap-xhdpi": (96, 96),
        "mipmap-xxhdpi": (144, 144),
        "mipmap-xxxhdpi": (192, 192)
    }
    for dir_name in android_dirs.keys():
        android_dir = os.path.join(output_directory, "android", dir_name)
        if not os.path.exists(android_dir):
            os.makedirs(android_dir)

    # Generate resized icons for AppIcon.appiconset based on the JSON specification
    appiconset_sizes = [
        (60, 60), (40, 40), (120, 120), (57, 57), (29, 29), (87, 87), (114, 114), 
        (40, 40), (20, 20), (1024, 1024), (80, 80), (72, 72), (152, 152), (50, 50), 
        (58, 58), (76, 76), (167, 167), (86, 86), (44, 44), (45, 45), (46, 46), 
        (50, 50), (98, 98), (108, 108), (24, 24), (28, 28), (33, 33), 
        (128, 128), (256, 256), (512, 512), (32, 32), (16, 16), (64, 64)
    ]

    for size in appiconset_sizes:
        try:
            resized_icon = original_icon.resize((int(size[0]), int(size[1])), Image.LANCZOS)
            output_path = os.path.join(appiconset_dir, f'{int(size[0])}.png')
            resized_icon.save(output_path)
        except Exception as e:
            print(f"Error resizing image to {size} for AppIcon.appiconset: {e}")

    # Generate resized icons for android
    for dir_name, size in android_dirs.items():
        try:
            resized_icon = original_icon.resize(size, Image.LANCZOS)
            output_path = os.path.join(output_directory, "android", dir_name, f'icon_{size[0]}x{size[1]}.png')
            resized_icon.save(output_path)
        except Exception as e:
            print(f"Error resizing image to {size} for android: {e}")

    # Generate appstore and playstore images
    try:
        resized_icon_appstore = original_icon.resize((1024, 1024), Image.LANCZOS)
        resized_icon_playstore = original_icon.resize((512, 512), Image.LANCZOS)
        resized_icon_appstore.save(os.path.join(output_directory, 'appstore.png'))
        resized_icon_playstore.save(os.path.join(output_directory, 'playstore.png'))
    except Exception as e:
        print(f"Error resizing image for appstore or playstore: {e}")

    # Save the JSON file for AppIcon.appiconset
    json_path = os.path.join(appiconset_dir, "Contents.json")
    with open(json_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
