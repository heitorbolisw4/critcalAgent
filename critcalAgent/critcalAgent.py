import os
import argparse
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize ChatGroq
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

chat = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

def analyze_code(code_content, file_path="snippet"):
    """
    Analyzes a piece of code for security vulnerabilities using the LLM.
    """
    system_prompt = (
        "Você é um engenheiro de segurança AppSec especialista em PHP e aplicações web estáticas "
        "(HTML, CSS e JavaScript). "
        "Analise o código fornecido em busca de vulnerabilidades de segurança, especialmente SQL Injection, "
        "XSS e problemas de validação de entrada em páginas estáticas. "
        "Responda sempre em português com um relatório conciso contendo: "
        "1. Tipo de vulnerabilidade, 2. Linha (aprox.), 3. Gravidade, 4. Sugestão de correção. "
        "Se não houver vulnerabilidades relevantes, escreva 'Nenhuma vulnerabilidade significativa detectada'."
    )
    
    # Use {code_content} as a placeholder for the input variable
    human_message = "Arquivo: {file_path}\n\nCódigo:\n```{code_content}```"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_message)
    ])
    
    chain = prompt | chat
    try:
        # Pass the actual content as variables to avoid formatting issues with curly braces in code
        response = chain.invoke({"file_path": file_path, "code_content": code_content})
        return response.content
    except Exception as e:
        return f"Error analyzing {file_path}: {str(e)}"

def scan_directory(path, extensions=['.php', '.html', '.htm', '.js', '.css']):
    """
    Recursively scans a directory for files with given extensions.
    """
    files_to_scan = []
    for root, _, files in os.walk(path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                files_to_scan.append(os.path.join(root, file))
    return files_to_scan

def generate_report(results, output_file="security_report.md"):
    """
    Generates a markdown report from the analysis results.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Security Analysis Report\n\n")
        for file_path, analysis in results.items():
            f.write(f"## File: `{file_path}`\n\n")
            f.write(analysis)
            f.write("\n\n---\n\n")
    print(f"Report generated: {output_file}")

def interactive_mode():
    """
    Runs the agent in interactive CLI mode.
    """
    print("CRITICAL AGENT: Interactive Mode (Type 'x' to exit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'x':
            break
        
        # In interactive mode, we treat the input as a code snippet or question
        analysis = analyze_code(user_input)
        print(f"Agent:\n{analysis}\n")

def main():
    parser = argparse.ArgumentParser(description="Critical Agent - AppSec Scanner")
    parser.add_argument("--scan", help="Path to the project directory to scan (or project name if in PROJECTS_ROOT)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()

    if args.scan:
        # Path resolution logic
        scan_path = args.scan
        
        # 1. Check if it's an absolute path or existing relative path
        if os.path.exists(scan_path):
            final_path = scan_path
        else:
            # 2. Try to resolve using PROJECTS_ROOT
            projects_root = os.getenv('PROJECTS_ROOT')
            if projects_root:
                potential_path = os.path.join(projects_root, scan_path)
                if os.path.exists(potential_path):
                    final_path = potential_path
                else:
                    print(f"Error: Project not found at '{scan_path}' or '{potential_path}'")
                    return
            else:
                print(f"Error: Path '{scan_path}' does not exist and PROJECTS_ROOT is not set.")
                return

        print(f"Scanning project at: {os.path.abspath(final_path)}")
        files = scan_directory(final_path)
        if not files:
            print("No matching files found.")
            return
        
        print(f"Found {len(files)} files. Starting analysis...")
        results = {}
        for file_path in files:
            print(f"Analyzing {file_path}...")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                results[file_path] = analyze_code(content, file_path)
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
        
        generate_report(results)
        
    else:
        # Default to interactive mode if no args provided or explicitly requested
        interactive_mode()

if __name__ == "__main__":
    main()
