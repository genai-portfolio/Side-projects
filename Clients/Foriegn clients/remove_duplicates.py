import os
import hashlib
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def get_file_hash(file_path):
    """Calculate MD5 hash of a file to check for duplicate content"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"    ⚠ Error reading {file_path}: {e}")
        return None

def find_csv_files(search_dirs):
    """Find all CSV files in the specified directories"""
    csv_files = []
    for directory in search_dirs:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith('.csv'):
                        file_path = os.path.join(root, file)
                        csv_files.append(file_path)
    return csv_files

def normalize_filename(filename):
    """Normalize filename to detect duplicates like 'Alabama.csv' and 'Alabama (1).csv'"""
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Remove patterns like " (1)", " (2)", etc.
    name = re.sub(r'\s*\(\d+\)\s*$', '', name)
    return name.lower().strip()

def find_duplicates_by_name(csv_files):
    """Find duplicates by filename patterns"""
    name_groups = defaultdict(list)
    
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        normalized = normalize_filename(filename)
        name_groups[normalized].append(file_path)
    
    # Return groups with more than one file
    duplicates = {name: files for name, files in name_groups.items() if len(files) > 1}
    return duplicates

def find_duplicates_by_content(csv_files):
    """Find duplicates by file content (hash)"""
    hash_groups = defaultdict(list)
    
    print("\n[2] Checking file contents for duplicates...")
    for i, file_path in enumerate(csv_files, 1):
        print(f"    Checking {i}/{len(csv_files)}: {os.path.basename(file_path)}")
        file_hash = get_file_hash(file_path)
        if file_hash:
            hash_groups[file_hash].append(file_path)
    
    # Return groups with more than one file
    duplicates = {file_hash: files for file_hash, files in hash_groups.items() if len(files) > 1}
    return duplicates

def get_file_info(file_path):
    """Get file modification time and size"""
    try:
        stat = os.stat(file_path)
        return {
            'path': file_path,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'filename': os.path.basename(file_path)
        }
    except:
        return None

def remove_duplicates(duplicate_groups, keep_oldest=False):
    """Remove duplicate files, keeping the most recent (or oldest if specified)"""
    removed_count = 0
    removed_size = 0
    
    for group_name, files in duplicate_groups.items():
        if len(files) <= 1:
            continue
        
        print(f"\n  Found {len(files)} duplicates for: {group_name}")
        
        # Get file info for all duplicates
        file_infos = []
        for file_path in files:
            info = get_file_info(file_path)
            if info:
                file_infos.append(info)
        
        if len(file_infos) <= 1:
            continue
        
        # Sort by modification time (newest first, or oldest if keep_oldest=True)
        file_infos.sort(key=lambda x: x['modified'], reverse=not keep_oldest)
        
        # Keep the first one (most recent or oldest)
        keep_file = file_infos[0]
        print(f"    ✓ Keeping: {keep_file['filename']} (Modified: {keep_file['modified'].strftime('%Y-%m-%d %H:%M:%S')})")
        
        # Remove the rest
        for file_info in file_infos[1:]:
            try:
                file_size = file_info['size']
                os.remove(file_info['path'])
                removed_count += 1
                removed_size += file_size
                print(f"    ✗ Removed: {file_info['filename']} (Modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')})")
            except Exception as e:
                print(f"    ⚠ Could not remove {file_info['filename']}: {e}")
    
    return removed_count, removed_size

def main():
    print("=" * 60)
    print("CSV Duplicate File Remover")
    print("=" * 60)
    
    # Define search directories
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, "data")
    downloads_dir = os.path.join(current_dir, "downloads")
    
    # Default Chrome downloads folder (Windows)
    chrome_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Priority: data folder first, then current directory, then downloads
    search_directories = []
    
    # Add data folder (primary location)
    if os.path.exists(data_dir):
        search_directories.append(data_dir)
    
    # Add other directories if they exist
    if os.path.exists(current_dir):
        search_directories.append(current_dir)
    if os.path.exists(downloads_dir):
        search_directories.append(downloads_dir)
    if os.path.exists(chrome_downloads):
        search_directories.append(chrome_downloads)
    
    print(f"\n[1] Searching for CSV files in:")
    for i, directory in enumerate(search_directories, 1):
        if os.path.exists(directory):
            if "data" in directory.lower():
                print(f"    ✓ {directory} (PRIMARY LOCATION)")
            else:
                print(f"    ✓ {directory}")
        else:
            print(f"    ✗ {directory} (not found)")
    
    # If data directory doesn't exist, warn user
    if not os.path.exists(data_dir):
        print(f"\n    ⚠ WARNING: Data folder not found at: {data_dir}")
        print(f"    Please ensure CSV files are in the 'data' folder.")
    
    # Find all CSV files
    csv_files = find_csv_files(search_directories)
    
    if not csv_files:
        print("\n✗ No CSV files found in the specified directories.")
        return
    
    print(f"\n✓ Found {len(csv_files)} CSV file(s)")
    
    # Find duplicates by name
    print("\n[2] Checking for duplicate filenames...")
    name_duplicates = find_duplicates_by_name(csv_files)
    
    if name_duplicates:
        print(f"✓ Found {len(name_duplicates)} group(s) with duplicate filenames")
    else:
        print("✓ No duplicate filenames found")
    
    # Find duplicates by content
    content_duplicates = find_duplicates_by_content(csv_files)
    
    if content_duplicates:
        print(f"\n✓ Found {len(content_duplicates)} group(s) with duplicate content")
    else:
        print("\n✓ No duplicate content found")
    
    # Combine all duplicates
    all_duplicates = {}
    
    # Add name-based duplicates
    for name, files in name_duplicates.items():
        all_duplicates[f"name_{name}"] = files
    
    # Add content-based duplicates (but avoid double-counting)
    for file_hash, files in content_duplicates.items():
        # Only add if not already in name duplicates
        already_covered = False
        for name, name_files in name_duplicates.items():
            if set(files).issubset(set(name_files)):
                already_covered = True
                break
        if not already_covered and len(files) > 1:
            all_duplicates[f"content_{file_hash[:8]}"] = files
    
    if not all_duplicates:
        print("\n" + "=" * 60)
        print("✓ No duplicates found! All files are unique.")
        print("=" * 60)
        return
    
    print(f"\n[3] Summary: Found {len(all_duplicates)} duplicate group(s)")
    
    # Ask user preference
    print("\n[4] Removal Strategy:")
    print("    Option 1: Keep the MOST RECENT file (recommended)")
    print("    Option 2: Keep the OLDEST file")
    
    choice = input("\nEnter choice (1 or 2, default=1): ").strip()
    keep_oldest = (choice == "2")
    
    strategy = "oldest" if keep_oldest else "most recent"
    print(f"\n[5] Removing duplicates (keeping {strategy} file)...")
    
    # Remove duplicates
    removed_count, removed_size = remove_duplicates(all_duplicates, keep_oldest=keep_oldest)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Files removed: {removed_count}")
    print(f"✓ Space freed: {removed_size / (1024*1024):.2f} MB")
    print("=" * 60)
    
    if removed_count > 0:
        print("\n✓ Duplicate removal completed successfully!")
    else:
        print("\n⚠ No files were removed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Process interrupted by user.")
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()