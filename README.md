# MusicBee to Rekordbox Playlist Folders fix
## The Problem
Rekordbox can import playlist structures from iTunes by reading the "iTunes Music Library.xml" file. MusicBee (v3.6.8906) can export a compatible XML file, theoretically allowing users to maintain their library organization in MusicBee rather than iTunes. However, while root-level playlists sync correctly, playlist folders appear empty in Rekordbox, making the folder structure unusable.

## Quick Solution
1. Download the `.exe` file.
2. Place it in the same folder as your MusicBee-generated "iTunes Music Library.xml" file
3. Run the `.exe` file - it will create "iTunes Music Library for Rekordbox.xml"
4. In Rekordbox, go to File -> Advanced -> Database -> iTunes -> iTunes Library File
5. Select the new "iTunes Music Library for Rekordbox.xml" file
6. Reload iTunes library in Rekordbox

## Advanced Usage
The executable can be run from the command line with optional arguments:

```powershell
musicbee_rekordbox_playlistfolder_fix.exe --input "custom_input.xml" --output "custom_output.xml"

Available arguments:

    --input: Specify custom input XML file path (default: "iTunes Music Library.xml")
    --output: Specify custom output XML file path (default: "iTunes Music Library for Rekordbox.xml")
```

**Note:** Whenever your MusicBee library is updated, to see the new changes in Rekordbox, the .exe file will need to be re-run.

## Technical Details
The issue stems from the `<key>Playlist Persistent ID</key>` XML entries, which are typically managed by iTunes' binary ".itl" file. This fix selectively removes these IDs from regular playlists while preserving them in folder playlists, allowing proper parent-child relationships between folders and their contained playlists.

## Development
The source code (`.py` script) is included in this repository. Feel free to review, modify, or improve it.

### Building from Source
If you want to build the executable yourself:
1. Ensure Python is installed
2. Install PyInstaller: `pip install pyinstaller`
3. Run: `pyinstaller --onefile musicbee_rekordbox_playlistfolder_fix`