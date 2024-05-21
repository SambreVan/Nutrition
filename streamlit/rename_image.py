import os


extracted_path = '../img.zip'


files = os.listdir(extracted_path)


for i, file_name in enumerate(files):

    file_extension = os.path.splitext(file_name)[1]

    new_file_name = f"{i+1}{file_extension}"

    old_file_path = os.path.join(extracted_path, file_name)
    new_file_path = os.path.join(extracted_path, new_file_name)

    os.rename(old_file_path, new_file_path)

print("Files have been renamed successfully.")
