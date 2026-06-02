import os
import json
import yaml

def migrate():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excluded_dirs = ['.git', '.github', 'scripts', 'docs', 'assets', 'zzz']

    migrated_count = 0

    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if not os.path.isdir(category_path) or category in excluded_dirs:
            continue
            
        for skill_dir in os.listdir(category_path):
            skill_path = os.path.join(category_path, skill_dir)
            if not os.path.isdir(skill_path):
                continue
                
            manifest_file = os.path.join(skill_path, "manifest.json")
            if os.path.exists(manifest_file):
                try:
                    with open(manifest_file, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                    
                    skill_md_path = os.path.join(skill_path, "SKILL.md")
                    
                    # Create SKILL.md
                    with open(skill_md_path, 'w', encoding='utf-8') as f:
                        f.write("---\n")
                        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
                        
                        # Add a dummy logic.wasm link if one exists in the dir
                        has_wasm = os.path.exists(os.path.join(skill_path, "logic.wasm"))
                        has_mcp = os.path.exists(os.path.join(skill_path, "connector.js")) or os.path.exists(os.path.join(skill_path, "connector.py"))
                        
                        if has_wasm or has_mcp:
                            f.write("\nlinks:\n")
                            if has_wasm:
                                f.write("  wasm: \"./logic.wasm\"\n")
                            if has_mcp:
                                f.write("  mcp: \"./connector.js\"\n") # Simplified
                                
                        f.write("---\n\n")
                        f.write(f"# {manifest.get('name', skill_dir)}\n\n")
                        f.write(f"{manifest.get('description', '')}\n")
                        
                    # Delete old manifest.json
                    os.remove(manifest_file)
                    print(f"Migrated: {category}/{skill_dir}")
                    migrated_count += 1
                except Exception as e:
                    print(f"Error migrating {manifest_file}: {e}")

    print(f"Migration complete. {migrated_count} skills migrated.")

if __name__ == "__main__":
    migrate()
