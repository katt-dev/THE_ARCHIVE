class VirtualFileSystem:
    def __init__(self):
        self.nodes = {
            "/": {"type": "dir", "metadata": {"hidden": False}},
            "/README.txt": {
                "type": "file", 
                "content": "ARCHIVE INITIALIZED.\nDo not trust the timestamps.", 
                "encrypted": False, 
                "required_key": None,
                "metadata": {"corrupted": False, "read": False}
            },
            "/documents": {"type": "dir", "metadata": {"hidden": False}},
            "/encrypted": {"type": "dir", "metadata": {"hidden": False}},
            "/system": {"type": "dir", "metadata": {"hidden": False}},
        }

    def get_node(self, path: str) -> dict:
        return self.nodes.get(path)

    def list_dir(self, path: str) -> list:
        if not path.endswith("/"):
            path += "/"
        if path == "//": 
            path = "/"
            
        items = []
        for p, data in self.nodes.items():
            if p.startswith(path) and p != path:
                rel = p[len(path):]
                if "/" not in rel:
                    items.append({"name": rel, "data": data})
        return items

    def resolve_path(self, current_dir: str, target: str) -> str:
        if target == "/":
            return "/"
        
        parts = target.split("/")
        if target.startswith("/"):
            resolved = []
        else:
            resolved = [p for p in current_dir.split("/") if p]
            
        for part in parts:
            if part == "" or part == ".":
                continue
            elif part == "..":
                if resolved:
                    resolved.pop()
            else:
                resolved.append(part)
                
        return "/" + "/".join(resolved)
