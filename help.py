import os

def replace_in_file(file_path, old_str, new_str):
    with open(file_path, 'r') as file:
        
        content = file.read()
    content = content.replace(old_str, new_str)
    with open(file_path, 'w') as file:
        file.write(content)

def search_and_replace(directory_path, old_str, new_str):
    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            try:
                replace_in_file(file_path, old_str, new_str)
            except:
                pass
        for subfolder in subfolders:
            subfolder_path = os.path.join(foldername, subfolder)
            new_subfolder = subfolder.replace(old_str, new_str)
            os.rename(subfolder_path, os.path.join(foldername, new_subfolder))

if __name__ == "__main__":
    directory_path = input("Enter the directory path to search and replace: ")
    old_str = input("input oldstr: ")
    new_str = "upscale"

    search_and_replace(directory_path, old_str.lower(), new_str.lower())
    print("Search and replace completed.")