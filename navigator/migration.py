import re
import requests
import datetime
import json
from pathlib import Path
import time

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/api/projects"
MARKDOWN_FILE = Path(__file__).parent.parent / "项目导航.md"

STATUS_MAP = {
    "✅": "完成",
    "🚧": "进行中",
    "🔍": "研究中",
    "📚": "理论归档",
    "🎯": "规划中",
}

# --- Heuristic Mappings ---
# Based on status, we infer maturity and project type
MATURITY_MAP = {
    "完成": "High",
    "进行中": "High",
    "规划中": "Medium",
    "研究中": "Medium",
    "理论归档": "Low",
}

PROJECT_TYPE_MAP = {
    "完成": "工具开发",
    "进行中": "工具开发",
    "规划中": "工具开发",
    "研究中": "理论分析",
    "理论归档": "理论分析",
}


def parse_markdown():
    """Parses the markdown file to extract project data."""
    print(f"Reading markdown file from: {MARKDOWN_FILE}")
    if not MARKDOWN_FILE.exists():
        print(f"Error: Markdown file not found at {MARKDOWN_FILE}")
        return []

    content = MARKDOWN_FILE.read_text(encoding="utf-8")
    
    # Extract the main project table
    table_regex = r"## 📋 项目概览\s*\|([\s\S]*?)\s*## 🚀 项目详情"
    table_match = re.search(table_regex, content)
    if not table_match:
        print("Error: Could not find the project overview table.")
        return []

    table_content = table_match.group(1)
    rows = table_content.strip().split("\n")[2:] # Skip header and separator

    projects = []
    for row in rows:
        if not row.strip() or "---" in row:
            continue
        
        parts = [p.strip() for p in row.split("|") if p.strip()]
        if len(parts) < 4:
            continue

        # --- Extract from table ---
        # 1. Name and Readme Path
        name_part = parts[0]
        name_match = re.search(r"\[(.*?)\]\((.*?)\)", name_part)
        if not name_match:
            continue
        name = name_match.group(1)
        readme_path = name_match.group(2)

        # 2. Status
        status_part = parts[1]
        status_icon = status_part.split(" ")[0]
        status_text = STATUS_MAP.get(status_icon, "未知")

        # 3. Created Date
        date_part = parts[3]
        try:
            # Handles "YYYY-M" and "YYYY-MM" format
            year, month = map(int, date_part.split('-'))
            created_date = datetime.date(year, month, 1)
        except ValueError:
            created_date = datetime.date.today()
            print(f"Warning: Could not parse date '{date_part}' for project '{name}'. Using today's date.")


        # --- Extract from details section ---
        description = ""
        # The section header in the markdown is `### Project Name`
        # The key parts are bolded, e.g., **🎯 项目描述**:
        # We look for the description block and stop at the next double newline followed by the start of another bolded line.
        desc_regex = rf"###\s*{re.escape(name)}[\s\S]*?\*\*🎯 项目描述\*\*:\s*([\s\S]*?)(?=\n\n\*\*)"
        desc_match = re.search(desc_regex, content)
        if desc_match:
            description = desc_match.group(1).strip()
        else:
            # Fallback for projects at the very end of the file or with different structures
            desc_regex_fallback = rf"###\s*{re.escape(name)}[\s\S]*?\*\*🎯 项目描述\*\*:\s*([\s\S]*?)(?=###\s*)"
            desc_match_fallback = re.search(desc_regex_fallback, content)
            if desc_match_fallback:
                description = desc_match_fallback.group(1).strip()
            else:
                print(f"Warning: Could not find description for project '{name}'.")

        # --- Infer data ---
        maturity = MATURITY_MAP.get(status_text, "Unknown")
        project_type = PROJECT_TYPE_MAP.get(status_text, "Unknown")

        project_data = {
            "name": name,
            "readme_path": readme_path,
            "status": status_text,
            "created_date": created_date.isoformat(),
            "description": description,
            "maturity": maturity,
            "project_type": project_type,
        }
        projects.append(project_data)

    print(f"Successfully parsed {len(projects)} projects.")
    return projects

def migrate_to_db(projects):
    """Sends parsed project data to the API."""
    if not projects:
        print("No projects to migrate.")
        return

    print("\nStarting migration...")
    succeeded = 0
    failed = 0
    
    headers = {"Content-Type": "application/json"}

    for project in projects:
        try:
            response = requests.post(API_URL, data=json.dumps(project), headers=headers)
            if response.status_code == 200:
                print(f"  ✅ Successfully added '{project['name']}'")
                succeeded += 1
            elif response.status_code == 409: # Conflict for duplicates
                 print(f"  ⚠️ Project '{project['name']}' already exists. Skipping.")
                 succeeded +=1 # Count as success as it's already there
            else:
                print(f"  ❌ Failed to add '{project['name']}'. Status: {response.status_code}")
                print(f"     Response: {response.text}")
                failed += 1
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Failed to add '{project['name']}'. Error: {e}")
            failed += 1
        
        # Add a delay to prevent overwhelming the server
        time.sleep(0.5)
            
    print("\n--- Migration Summary ---")
    print(f"Total projects processed: {len(projects)}")
    print(f"Succeeded: {succeeded}")
    print(f"Failed: {failed}")
    print("--------------------------")
    if failed > 0:
        print("Some projects could not be migrated. Please check the errors above.")
    else:
        print("Migration completed successfully!")


if __name__ == "__main__":
    project_data = parse_markdown()
    if project_data:
        # Make sure server is running
        try:
            requests.get(API_URL.replace("/api/projects", "/"), timeout=2)
        except requests.exceptions.ConnectionError:
            print("\n🚨 Error: The backend server is not running or not accessible at a '{API_URL}'.")
            print("Please start the server first by running this command in another terminal:")
            print("uvicorn navigator.app.main:app --reload")
            exit(1)
        migrate_to_db(project_data) 