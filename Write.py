import os
import zipfile

def modify_hex_reverse(file_path):
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        content = content.replace(b"9", b"1").replace(b"8", b"2").replace(b"4", b"3").replace(b"5", b"7")
        with open(file_path, "wb") as file:
            file.write(content)
    except Exception as e:
        print(f"Something went wrong: {e}")

def xor_encrypt(data, key):
    return bytearray([b ^ key for b in data])

def create_custom_nex(zip_path, output_path, key):
    try:
        with open(zip_path, "rb") as file:
            content = file.read()
        
        encrypted_content = xor_encrypt(content, key)
        
        with open(output_path, "wb") as file:
            file.write(b"NXF_HEADER" + encrypted_content + b"NXF_FOOTER")
    except Exception as e:
        print(f"Something went wrong: {e}")

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python Write.py <file.zip>")
        return

    filearg1 = sys.argv[1]
    fname = os.path.splitext(filearg1)[0]

    try:
        with zipfile.ZipFile(filearg1, 'r') as zip_file:
            zip_file.extractall(f"assets/games/{fname}")

        manifest_path = f"assets/games/{fname}/manifest.json"
        if os.path.exists(manifest_path):
            modify_hex_reverse(manifest_path)
        else:
            error = "manifest.json not found in the zip file."
            with open("error.txt", "w") as log_file:
                log_file.write(error)
            return

        nex_file_path = f"{fname}.nex"
        with zipfile.ZipFile(nex_file_path, 'w') as nex_file:
            for folder_name, subfolders, filenames in os.walk(f"assets/games/{fname}"):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    nex_file.write(file_path, os.path.relpath(file_path, f"assets/games/{fname}"))

        # Encrypt the .nex file
        create_custom_nex(nex_file_path, nex_file_path, key=0x55)

    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()