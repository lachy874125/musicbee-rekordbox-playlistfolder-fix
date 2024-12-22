"""
MusicBee to Rekordbox Playlist Folders Fix

This script fixes the MusicBee-generated "iTunes Music Library.xml" file to make
playlist folders work correctly in Rekordbox. Without this fix, playlist folders
appear empty in Rekordbox even though they contain playlists in MusicBee.

The script removes 'Playlist Persistent ID' entries from regular playlists while
preserving them in folder playlists, allowing proper folder hierarchy in Rekordbox.
"""

import xml.etree.ElementTree as ET
import shutil
import os
import sys
import argparse
from datetime import datetime

def log_message(message):
    """Print a timestamped log message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Fix MusicBee XML for Rekordbox playlist folders.')
    parser.add_argument('--input', default="iTunes Music Library.xml",
                      help='Input XML file path (default: iTunes Music Library.xml)')
    parser.add_argument('--output', default="iTunes Music Library for Rekordbox.xml",
                      help='Output XML file path (default: iTunes Music Library for Rekordbox.xml)')
    return parser.parse_args()

def check_input_file(input_file):
    """Verify input file exists and is readable."""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    if not os.path.isfile(input_file):
        raise ValueError(f"Input path is not a file: {input_file}")
    if not os.access(input_file, os.R_OK):
        raise PermissionError(f"Cannot read input file: {input_file}")

def process_xml_file(input_file, output_file):
    """Process the XML file and create modified version."""
    log_message(f"Processing {input_file}")
    
    # Create a temporary file
    temp_file = input_file + ".temp"
    shutil.copy2(input_file, temp_file)

    try:
        # Read the XML declaration lines
        with open(input_file, 'r', encoding='UTF-8') as f:
            first_line = f.readline().strip()
            second_line = f.readline().strip()

        # Parse the XML file
        tree = ET.parse(temp_file)
        root = tree.getroot()

        # Find the Playlists array
        playlists = root.find("dict/array")
        if playlists is None:
            raise ValueError("Could not find playlists array in XML file")

        total_playlists = len(playlists)
        
        # Process each playlist
        for playlist in playlists:
            # Check if this is a folder playlist
            is_folder = any(
                key.text == "Folder" 
                for key in playlist.findall("key")
            )

            # Remove Playlist Persistent ID from non-folder playlists
            if not is_folder:
                i = 0
                while i < len(playlist):
                    if (i + 1 < len(playlist) and 
                        playlist[i].text == "Playlist Persistent ID"):
                        # Remove both the key and its value
                        playlist.remove(playlist[i+1])
                        playlist.remove(playlist[i])
                        break
                    i += 2

        # Write the modified XML
        tree_str = ET.tostring(root, encoding='UTF-8', xml_declaration=False)
        
        with open(output_file, 'w', encoding='UTF-8') as f:
            f.write(first_line + '\n')
            f.write(second_line + '\n')
            f.write(tree_str.decode('UTF-8'))

        log_message(f"Modified all regular playlists")
        log_message(f"Created {output_file}")

    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

def main():
    """Main execution function."""
    try:
        args = parse_arguments()
        check_input_file(args.input)
        process_xml_file(args.input, args.output)
        log_message("Processing complete")
    except Exception as e:
        log_message(f"Error: {str(e)}")
        sys.exit(1)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
