import os
import json
import subprocess
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    # Detect modified package.json files
    # We look at the diff from the previous commit
    diff_output = run_cmd("git diff --name-only HEAD^ HEAD")
    changed_files = diff_output.split('\n')
    
    packages_to_build = []
    
    for file in changed_files:
        if file.endswith("package.json") and ("extensions/" in file or "skills/" in file or "plugins/" in file or "mcp/" in file or "souls/" in file):
            packages_to_build.append(file)
            
    if not packages_to_build:
        print("No packages changed.")
        # Output empty matrix to GitHub step output
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write("should_run=false\n")
            f.write("matrix={}\n")
        return

    matrix_jobs = []
    
    for pkg_path in packages_to_build:
        if not os.path.exists(pkg_path):
            continue
            
        with open(pkg_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        pkg_id = data.get("id", "unknown")
        build_type = data.get("build_type", "none")
        version = data.get("latest_version", "1.0.0")
        github_action = data.get("github_action", True)
        
        if not github_action:
            print(f"Skipping {pkg_id} as github_action is set to false.")
            continue
        
        # Determine prefix based on category path
        category = pkg_path.split('/')[0]
        prefix = "ext"
        if category == "skills": prefix = "skill"
        elif category == "plugins": prefix = "plugin"
        elif category == "mcp": prefix = "mcp"
        elif category == "souls": prefix = "soul"
        
        tag_name = f"{prefix}-{pkg_id}"
        pkg_dir = os.path.dirname(pkg_path)
        
        # ALWAYS generate a Master ZIP job for every package
        matrix_jobs.append({
            "id": pkg_id,
            "target": "master-zip",
            "os": "ubuntu-latest",
            "version": version,
            "tag_name": tag_name,
            "pkg_dir": pkg_dir,
            "filename": f"{pkg_id}-files-v{version}.zip",
            "is_zip": "true"
        })
        
        # Generate matrix permutations based on build_type
        if build_type == "binary":
            builds_os = ["windows", "macos", "linux"]
            if "versions" in data and version in data["versions"]:
                builds_os = data["versions"][version].get("builds_os", ["windows", "macos", "linux"])
                
            if "windows" in builds_os:
                matrix_jobs.append({
                    "id": pkg_id,
                    "target": "windows-x64",
                    "os": "windows-latest",
                    "version": version,
                    "tag_name": tag_name,
                    "pkg_dir": pkg_dir,
                    "filename": f"{pkg_id}_windows_x64_v{version}.dll",
                    "is_zip": "false"
                })
            if "linux" in builds_os:
                matrix_jobs.append({
                    "id": pkg_id,
                    "target": "linux-x64",
                    "os": "ubuntu-latest",
                    "version": version,
                    "tag_name": tag_name,
                    "pkg_dir": pkg_dir,
                    "filename": f"lib{pkg_id}_linux_x64_v{version}.so",
                    "is_zip": "false"
                })
            if "macos" in builds_os:
                matrix_jobs.append({
                    "id": pkg_id,
                    "target": "macos-arm64",
                    "os": "macos-14",
                    "version": version,
                    "tag_name": tag_name,
                    "pkg_dir": pkg_dir,
                    "filename": f"lib{pkg_id}_macos_arm64_v{version}.dylib",
                    "is_zip": "false"
                })
        elif build_type == "wasm":
            matrix_jobs.append({
                "id": pkg_id,
                "target": "wasm32",
                "os": "ubuntu-latest",
                "version": version,
                "tag_name": tag_name,
                "pkg_dir": pkg_dir,
                "filename": f"{pkg_id}_v{version}.wasm",
                "is_zip": "false"
            })
            
    matrix = {
        "include": matrix_jobs
    }
    
    matrix_json = json.dumps(matrix)
    print(f"Generated Matrix: {matrix_json}")
    
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write("should_run=true\n")
        f.write(f"matrix={matrix_json}\n")

if __name__ == "__main__":
    main()
