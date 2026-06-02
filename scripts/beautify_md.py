import os
import yaml

def beautify_skills():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excluded_dirs = ['.git', '.github', 'scripts', 'docs', 'assets', 'zzz']

    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if not os.path.isdir(category_path) or category in excluded_dirs:
            continue
            
        for skill_dir in os.listdir(category_path):
            skill_path = os.path.join(category_path, skill_dir)
            if not os.path.isdir(skill_path):
                continue
                
            skill_md_path = os.path.join(skill_path, "SKILL.md")
            if os.path.exists(skill_md_path):
                try:
                    with open(skill_md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.startswith('---'):
                        end_idx = content.find('---', 3)
                        if end_idx != -1:
                            frontmatter_str = content[3:end_idx]
                            manifest = yaml.safe_load(frontmatter_str)
                            
                            # Build a beautiful Markdown body
                            name = manifest.get('name', skill_dir)
                            desc = manifest.get('description', '')
                            triggers = manifest.get('triggers', {}).get('semantic', [])
                            perms = manifest.get('permissions', {})
                            links = manifest.get('links', {})
                            
                            trigger_list = "\n".join([f"- `{t}`" for t in triggers])
                            
                            # Format permissions nicely
                            fs_perm = "✅ Granted" if perms.get('filesystem') else "❌ Denied"
                            net_perm = "✅ Granted" if perms.get('network') else "❌ Denied"
                            lvl_perm = perms.get('level', 'None')
                            
                            # Check assets
                            has_wasm = "wasm" in links
                            asset_desc = "Runs high-performance Native WASM logic (`logic.wasm`) for zero-latency execution." if has_wasm else "Executes natively via Sovereign Agent."
                            
                            new_markdown = f"""---
{frontmatter_str.strip()}
---

# 🚀 {name.replace('-', ' ').title()}

> **{desc}**

## 📖 Overview
The `{name}` skill is a Sovereign native capability designed for the Cluaiz ecosystem. It operates seamlessly under the `{category}` category, providing highly optimized operations without relying on bloated external dependencies.

## 🎯 How to Use (Triggers)
You can invoke this skill autonomously by using any of the following semantic triggers in your conversation:
{trigger_list}

*(Entropy Threshold: {manifest.get('triggers', {}).get('entropy_threshold', 0.7)})*

## 🔒 Security & Permissions
This skill operates strictly within the Cluaiz Zero-Trust sandbox.
- **Filesystem Access:** {fs_perm}
- **Network Access:** {net_perm}
- **Access Level:** `{lvl_perm}`

## ⚙️ Under the Hood
**Soul Type:** `{manifest.get('soul_type', 'KV_CACHE')}`
{asset_desc}
"""
                            with open(skill_md_path, 'w', encoding='utf-8') as wf:
                                wf.write(new_markdown)
                                
                            print(f"Beautified: {skill_dir}")
                except Exception as e:
                    print(f"Failed to beautify {skill_md_path}: {e}")

if __name__ == "__main__":
    beautify_skills()
