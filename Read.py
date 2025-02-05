import os

def xor_decrypt(data, key):
    return bytearray([b ^ key for b in data])

def extract_custom_nex(nex_path, output_path, key):
    try:
        with open(nex_path, "rb") as file:
            content = file.read()
        
        # Remove custom header and footer
        if content.startswith(b"NXF_HEADER") and content.endswith(b"NXF_FOOTER"):
            content = content[len(b"NXF_HEADER"):-len(b"NXF_FOOTER")]
        else:
            raise ValueError("Invalid .nex file format")
        
        decrypted_content = xor_decrypt(content, key)
        
        with open(output_path, "wb") as file:
            file.write(decrypted_content)
    except Exception as e:
        print(f"Something went wrong: {e}")

def modify_hex(file_path):
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        content = content.replace(b"1", b"9").replace(b"2", b"8").replace(b"3", b"4").replace(b"7", b"5")
        with open(file_path, "wb") as file:
            file.write(content)
    except Exception as e:
        print(f"Something went wrong: {e}")

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python Read.py <file.nex>")
        return

    filearg1 = sys.argv[1]
    fname = os.path.splitext(filearg1)[0]

    try:
        zip_file_path = f"{fname}.zip"
        
        # Decrypt the .nex file
        extract_custom_nex(filearg1, zip_file_path, key=0x55)
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            zip_file.extractall(f"assets/games/{fname}")

        manifest_path = f"assets/games/{fname}/manifest.json"
        if os.path.exists(manifest_path):
            modify_hex(manifest_path)
        else:
            error = "manifest.json not found in the zip file."
            with open("error.txt", "w") as log_file:
                log_file.write(error)
            return

    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
