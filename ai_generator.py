import requests
import os
import trimesh
from dotenv import load_dotenv

load_dotenv()
THINGIVERSE_TOKEN = os.getenv("THINGIVERSE_TOKEN")

if not THINGIVERSE_TOKEN:
    raise ValueError("ERROR: THINGIVERSE_TOKEN not found in .env file!")

# Thingiverse expects the token in the Authorization header
HEADERS = {
    "Authorization": f"Bearer {THINGIVERSE_TOKEN}"
}


def generate_3d_model(prompt, output_filename="generated.obj"):
    print(f"[*] Searching Thingiverse for: '{prompt}'...")

    # 1. Search for the prompt (sorted by relevance)
    search_url = f"https://api.thingiverse.com/search/{prompt}?type=things&sort=relevant"
    response = requests.get(search_url, headers=HEADERS)

    if response.status_code != 200:
        print("Search error. API responded with:", response.text)
        return None

    data = response.json()
    hits = data.get("hits", [])

    if not hits:
        print(f"No results found for '{prompt}'.")
        return None

    # Take the first (most relevant) result
    first_thing_id = hits[0]["id"]
    print(f"[*] Hit found! Thing-ID: {first_thing_id}. Loading file list...")

    # 2. Fetch the actual files for this Thing
    files_url = f"https://api.thingiverse.com/things/{first_thing_id}/files"
    files_response = requests.get(files_url, headers=HEADERS)

    if files_response.status_code != 200:
        print("Error fetching files.")
        return None

    files_data = files_response.json()

    # 3. Find the first usable 3D file (.stl or .obj)
    target_file = None
    for f in files_data:
        # Some files are images, we only want 3D formats
        if f["name"].lower().endswith((".stl", ".obj")):
            target_file = f
            break

    if not target_file:
        print("The found model has no suitable 3D files.")
        return None

    download_url = target_file["download_url"]
    file_ext = target_file["name"].split(".")[-1].lower()
    temp_filename = f"temp_model.{file_ext}"

    print(f"[*] Downloading file: {target_file['name']}...")
    download_model(download_url, temp_filename)

    # 4. Convert if it's an STL file
    if file_ext == "stl":
        print("[*] Converting STL to OBJ (this may take a few seconds for large files)...")
        # trimesh loads the STL and merges it into a clean mesh
        mesh = trimesh.load(temp_filename, force='mesh')
        mesh.export(output_filename)
        os.remove(temp_filename)  # Delete temporary STL
        print(f"[*] Model successfully converted and saved as '{output_filename}'!")
    else:
        # If it's already an OBJ file, just rename it
        os.rename(temp_filename, output_filename)
        print(f"[*] Model successfully saved as '{output_filename}'!")

    return output_filename


def download_model(url, filename):
    # The actual download link also often requires authentication
    response = requests.get(url, headers=HEADERS)
    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    # Test call before integrating into main.py
    # generate_3d_model("cat")
    pass