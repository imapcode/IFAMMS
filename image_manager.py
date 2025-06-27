import os
import hashlib
from tkinter import Tk, filedialog
from PIL import Image

class ImageFile:
    def __init__(self, filename, path, size, img_format):
        self.filename = filename
        self.path = path
        self.size = size
        self.img_format = img_format

    def __lt__(self, other):
        return self.size < other.size

# ===== Linked List Implementation =====
class Node:
    def __init__(self, data):
        self.data = data  # This is an ImageFile object
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def to_list(self):
        lst = []
        temp = self.head
        while temp:
            lst.append(temp.data)
            temp = temp.next
        return lst

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def clear(self):
        self.head = None

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        # Swap first and last
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index].size < self.heap[parent].size:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        size = len(self.heap)

        if left < size and self.heap[left].size < self.heap[smallest].size:
            smallest = left
        if right < size and self.heap[right].size < self.heap[smallest].size:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def is_empty(self):
        return len(self.heap) == 0

# ======================================

def choose_directory():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Image Folder")
    root.destroy()
    return directory

def choose_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an Image File",
                                           filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")])
    root.destroy()
    return file_path

def get_image_files(directory):
    supported = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    files = []
    for file in os.listdir(directory):
        if file.lower().endswith(supported):
            path = os.path.join(directory, file)
            size = os.path.getsize(path)
            try:
                with Image.open(path) as img:
                    img_format = img.format
                    files.append(ImageFile(file, path, size, img_format))
            except:
                print(f"Skipping unreadable file: {file}")
    return files

def sort_images_by_size(images):
    min_heap = MinHeap()
    for img in images:
        min_heap.insert(img)
    sorted_list = []
    while not min_heap.is_empty():
        sorted_list.append(min_heap.extract_min())
    return sorted_list


def find_duplicate_images(images):
    hash_map = {}
    duplicates = []
    for img in images:
        with open(img.path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in hash_map:
                duplicates.append((img, hash_map[file_hash]))
            else:
                hash_map[file_hash] = img
    return duplicates, hash_map

def delete_duplicate_images(duplicates, hash_map):
    if not duplicates:
        print("No duplicates to delete.")
        return
    
    print("\nAvailable duplicates to delete:")
    for i, (dup_img, original) in enumerate(duplicates, 1):
        print(f"{i}. {dup_img.filename} (duplicate of {original.filename})")
    
    choice = input("\nEnter numbers to delete (comma-separated) or 'all' to delete all duplicates: ")
    if choice.lower() == 'all':
        for dup_img, _ in duplicates:
            try:
                os.remove(dup_img.path)
                print(f"Deleted: {dup_img.filename}")
            except Exception as e:
                print(f"Error deleting {dup_img.filename}: {e}")
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',') if x.strip()]
            for idx in indices:
                if 1 <= idx <= len(duplicates):
                    dup_img, _ = duplicates[idx-1]
                    try:
                        os.remove(dup_img.path)
                        print(f"Deleted: {dup_img.filename}")
                    except Exception as e:
                        print(f"Error deleting {dup_img.filename}: {e}")
                else:
                    print(f"Invalid index: {idx}")
        except ValueError:
            print("Invalid input. Please enter valid numbers or 'all'.")

def view_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            print(f"\nImage: {os.path.basename(image_path)}")
            print(f"Format: {img.format}")
            print(f"Size: {img.size}")
            print(f"Mode: {img.mode}")
    except:
        print("Unable to open image.")

def execute():
    image_list = LinkedList()
    duplicates = []
    hash_map = {}

    while True:
        print("\n========= Image File Handler ========= \n\n")
        print("[1] Load images from folder\n")
        print("[2] Sort images by file size\n")
        print("[3] Find duplicate images\n")
        print("[4] Delete duplicate images\n")
        print("[5] View image metadata\n")
        print("[6] Display selected image (metadata only)\n")
        print("[7] Exit\n")
        choice = input("Enter your choice: ")

        if choice == '1':
            folder = choose_directory()
            if folder:
                image_list.clear()
                for img in get_image_files(folder):
                    image_list.append(img)
                print(f"{len(image_list.to_list())} image(s) loaded from {folder}")
                duplicates = []
                hash_map = {}
            else:
                print("No folder selected.")

        elif choice == '2':
            if not image_list.head:
                print("Load images first.")
            else:
                sorted_images = sort_images_by_size(image_list.to_list())
                print("\nImages sorted by size:")
                for img in sorted_images:
                    print(f"{img.filename} - {img.size / 1024:.2f} KB - {img.img_format}")

        elif choice == '3':
            if not image_list.head:
                print("Load images first.")
            else:
                duplicates, hash_map = find_duplicate_images(image_list.to_list())
                if duplicates:
                    print("Duplicate images found:")
                    for dup_img, original in duplicates:
                        print(f"{dup_img.filename} is a duplicate of {original.filename}")
                else:
                    print("No duplicates found.")

        elif choice == '4':
            if not image_list.head:
                print("Load images first.")
            elif not duplicates:
                print("Find duplicates first using option 3.")
            else:
                delete_duplicate_images(duplicates, hash_map)

        elif choice == '5':
            if not image_list.head:
                print("Load images first.")
            else:
                for img in image_list:
                    print(f"{img.filename} - {img.size / 1024:.2f} KB - {img.img_format}")

        elif choice == '6':
            image_path = choose_file()
            if image_path:
                view_image_metadata(image_path)
            else:
                print("No file selected.")

        elif choice == '7':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    execute()
