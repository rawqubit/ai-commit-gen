import subprocess
import click
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Initialize OpenAI client
client = OpenAI()
console = Console()

@click.command()
@click.option('--staged', is_flag=True, help='Generate commit message for staged changes.')
def commit_gen(staged):
    """AI-powered Git commit message generator based on staged changes."""
    try:
        if staged:
            diff = subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
        else:
            diff = subprocess.check_output(['git', 'diff']).decode('utf-8')

        if not diff:
            console.print("[bold yellow]No changes detected.[/bold yellow]")
            return

        console.print("[bold blue]Analyzing changes...[/bold blue]")

        prompt = f"""
        Generate a concise and descriptive Git commit message based on the following diff.
        Follow conventional commit guidelines (e.g., feat:, fix:).
        Format your response in Markdown.

        Diff:
        ```diff
        {diff}
        ```
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {{"role": "system", "content": "You are an expert Git user."}},
                {{"role": "user", "content": prompt}}
            ]
        )
        commit_message = response.choices[0].message.content
        console.print(Markdown(commit_message))
    except Exception as e:
        console.print(f"[bold red]Error during commit message generation:[/bold red] {e}")

if __name__ == '__main__':
    commit_gen()
