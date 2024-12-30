import requests
import zipfile
import os
import shutil
import xml.etree.ElementTree as ET
from io import BytesIO

def download_and_extract_zip(url, extract_to):
    """Downloads a ZIP file from the given URL and extracts it to the given directory."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            zf.extractall(extract_to)
        print(f"Successfully downloaded and extracted '{url}' to '{extract_to}'")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading ZIP file: {e}")
    except zipfile.BadZipFile as e:
        print(f"Error extracting ZIP file: {e}")
    except Exception as e:
      print(f"An unexpected error occurred: {e}")


def extract_book_order(index_file):
    """Extracts the book order from TanachIndex.xml."""
    tree = ET.parse(index_file)
    root = tree.getroot()
    book_names = []
    for book in root.findall('.//book/names'):
      filename_tag = book.find('filename')
      if filename_tag is not None:
        filename = filename_tag.text
        book_names.append(filename)
    return book_names

def create_sequential_files(source_dir, dest_dir, book_order):
    """
    Reads XML files from the source directory, renames them with sequential numbers
    based on the provided book order, and copies them to the destination directory.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for i, filename in enumerate(book_order):
        source_filename = filename + ".xml"
        source_path = os.path.join(source_dir, source_filename)
        if os.path.exists(source_path):
            file_number = f"{i+1:02}"
            new_filename = f"{file_number}_{source_filename}"
            dest_path = os.path.join(dest_dir, new_filename)
            shutil.copy2(source_path, dest_path)
            print(f"Copied '{source_filename}' to '{new_filename}'")
        else:
            print(f"Warning: File '{source_filename}' not found in '{source_dir}'. Skipping.")

    print("Successfully created sequential files.")


if __name__ == "__main__":
    zip_url = "https://tanach.us/Books/Tanach.xml.zip"
    books_dir = "./Books"
    sequential_dir = "sequential"
    index_file = os.path.join(books_dir, "TanachIndex.xml")

    download_and_extract_zip(zip_url, "./")
    book_order = extract_book_order(index_file)
    create_sequential_files(books_dir, sequential_dir, book_order)
    print("process completed!")
