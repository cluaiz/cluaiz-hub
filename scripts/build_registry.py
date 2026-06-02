#!/usr/bin/env python3
import os
import json
import yaml
from pathlib import Path
from datetime import datetime, timezone

def parse_frontmatter(file_path):
    """Extract and parse YAML frontmatter from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if not content.startswith('---'):
            return None
            
        # Split by --- and get the second element (the frontmatter)
        parts = content.split('---')
        if len(parts) < 3:
            return None
            
        frontmatter_text = parts[1]
        data = yaml.safe_load(frontmatter_text)
        return data
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def scan_directory(base_path, expected_file="SKILL.md", item_type="skill"):
    """Scan a directory and return a lean dictionary mapping name to path and version."""
    items = {}
    base_dir = Path(base_path)
    
    if not base_dir.exists():
        return items
        
    for category_dir in base_dir.iterdir():
        if not category_dir.is_dir():
            continue
            
        if item_type == "soul" and (category_dir / expected_file).exists():
            item_path = category_dir
            frontmatter = parse_frontmatter(item_path / expected_file)
            if frontmatter and 'name' in frontmatter:
                name = frontmatter['name']
                version = str(frontmatter.get('version', '1.0.0'))
                direct_url = f"https://github.com/cluaiz/skills/releases/download/{name}-latest/{name}-v{version}.zip"
                items[name] = {
                    "latest": version,
                    "versions": {
                        version: direct_url
                    }
                }
            continue
            
        for item_dir in category_dir.iterdir():
            if not item_dir.is_dir():
                continue
                
            md_file = item_dir / expected_file
            if md_file.exists():
                frontmatter = parse_frontmatter(md_file)
                if frontmatter and 'name' in frontmatter:
                    name = frontmatter['name']
                    version = str(frontmatter.get('version', '1.0.0'))
                    
                    # Direct URL instead of template
                    direct_url = f"https://github.com/cluaiz/skills/releases/download/{name}-latest/{name}-v{version}.zip"
                    
                    items[name] = {
                        "latest": version,
                        "versions": {
                            version: direct_url
                        }
                    }
                    
    return items

def build_registry():
    """Build the full lean registry.json index."""
    print("Building Lean Cluaiz Skills Registry...")
    
    root_dir = Path(__file__).parent.parent
    
    skills = scan_directory(root_dir / "skills", "SKILL.md", "skill")
    plugins = scan_directory(root_dir / "plugins", "SKILL.md", "plugin")
    souls = scan_directory(root_dir / "souls", "SOUL.md", "soul")
    
    registry = {
        "_meta": {
            "updated": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        },
        "skills": skills,
        "plugins": plugins,
        "souls": souls
    }
    
    # Write to registry.json
    out_file = root_dir / "registry.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
        
    print(f"Registry built successfully at {out_file}")
    print(f"Found: {len(skills)} skills, {len(plugins)} plugins, {len(souls)} souls.")

if __name__ == "__main__":
    build_registry()
