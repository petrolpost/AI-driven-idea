import typer
from rich.prompt import Prompt, Confirm
from rich.console import Console
import requests
import datetime

app = typer.Typer()
console = Console()

API_URL = "http://127.0.0.1:8000/api/projects"

def create_project_interactive():
    name = Prompt.ask("Enter project name")
    
    project_type = Prompt.ask(
        "Enter project type",
        choices=["工具类", "分析类", "AI应用", "Web服务", "框架类", "理论类"],
        default="工具类"
    )

    maturity = Prompt.ask(
        "Enter maturity",
        choices=["🟢 高", "🟡 中", "🔴 低"],
        default="🟡 中"
    )

    status = Prompt.ask(
        "Enter status",
        choices=["✅ 完成", "🔍 研究中", "📋 规划中", "📚 已归档"],
        default="📋 规划中"
    )

    description = Prompt.ask("Enter description")

    project_slug = name.lower().replace(" ", "-")
    readme_path = f"ideaed-projects/{project_slug}/README.md"
    
    console.print(f"Generated readme path: [cyan]{readme_path}[/cyan]")
    
    project_data = {
        "name": name,
        "project_type": project_type,
        "maturity": maturity,
        "status": status,
        "description": description,
        "readme_path": readme_path,
        "created_date": datetime.date.today().isoformat()
    }

    return project_data

@app.command()
def add():
    """Add a new project interactively."""
    console.rule("[bold green]Add New Project[/bold green]")
    project_data = create_project_interactive()
    
    console.print("\n[bold]Project Data to be sent:[/bold]")
    console.print(project_data)

    if Confirm.ask("\nDo you want to create this project?"):
        try:
            response = requests.post(API_URL, json=project_data)
            response.raise_for_status()
            console.print("\n[bold green]✔ Project created successfully![/bold green]")
            console.print(response.json())
        except requests.exceptions.RequestException as e:
            console.print(f"\n[bold red]✖ Error creating project:[/bold red] {e}")

@app.command()
def hello():
    """A simple test command."""
    console.print("Hello from nav-admin!")

def main():
    app()

if __name__ == "__main__":
    main() 