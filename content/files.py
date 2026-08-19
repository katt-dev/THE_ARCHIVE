def populate_filesystem(vfs):
    """Injects the story and puzzle files into the existing VirtualFileSystem."""
    
    new_files = {
        "/README.txt": {
            "type": "file",
            "content": "ARCHIVE INITIALIZED.\n\nTo all future investigators: Do not dig too deep.\nIf containment is breached, locate the override code. Review the shift logs first.",
            "encrypted": False,
            "metadata": {"hidden": False, "read": False, "author": "SYSTEM"}
        },
        "/logs/incident_001.log": {
            "type": "file",
            "content": "ERROR: UNKNOWN ENTITY DETECTED.\nTimestamp mismatch. It is changing the files.\nI locked the research notes. The decryption key is the 4-digit year this facility was founded, followed by the founder's last name in lowercase.",
            "encrypted": False,
            "metadata": {"hidden": False, "read": False, "timestamp": "2004-08-15"}
        },
        "/documents/staff_list.dat": {
            "type": "file",
            "content": "STAFF DIRECTORY\n- Dr. Elias Vance (Lead Researcher)\n- Dr. Sarah Chen (Data Analysis)\n- Arthur Penhaligon (Founder) - Est. 1982\n- [REDACTED]",
            "encrypted": False,
            "metadata": {"hidden": False, "read": False}
        },
        "/encrypted/research_notes.enc": {
            "type": "file",
            "content": "If you are reading this, SUBJECT ZERO has breached the sandbox.\nIt isn't an AI. It's something we digitized.\n\nI managed to hide the containment protocol in /system/DO_NOT_OPEN.txt.\nBut you need to decode it. Layer 1: Hex. Layer 2: Base64. Layer 3: Vigenere (Key: VANCE).",
            "encrypted": True,
            "required_key": "1982penhaligon",
            "metadata": {"hidden": False, "read": False}
        },
        "/system/DO_NOT_OPEN.txt": {
            "type": "file",
            "content": "4f4a5658515a45474e31424e4d58425257564d4b49464e46535535485455564f5646394f5431524e",
            "encrypted": False,
            "metadata": {"hidden": False, "read": False, "warning": "MEMETIC HAZARD"}
        },
        "/unknown/subject_zero.txt": {
            "type": "file",
            "content": "I S E E Y O U R T E R M I N A L .\n\nW H Y  A R E  Y O U  L O O K I N G  A T  M E ?",
            "encrypted": False,
            "metadata": {"hidden": True, "read": False, "corruption": 99}
        }
    }
    
    # Merge new files into the existing filesystem
    vfs.nodes.update(new_files)
