from flask import Flask, render_template, request, redirect, url_for
import os
import markdown
from critcalAgent import scan_directory, analyze_code

app = Flask(__name__)

# Load PROJECTS_ROOT from environment (already loaded by critcalAgent, but good to have here too)
from dotenv import load_dotenv
load_dotenv()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_input = request.form.get('project_path')
        
        # Path resolution logic (duplicated from CLI for now, could be refactored)
        scan_path = project_input
        final_path = None
        
        if os.path.exists(scan_path):
            final_path = scan_path
        else:
            projects_root = os.getenv('PROJECTS_ROOT')
            if projects_root:
                potential_path = os.path.join(projects_root, scan_path)
                if os.path.exists(potential_path):
                    final_path = potential_path
        
        if not final_path:
            return render_template('index.html', error=f"Project not found: {project_input}")
        
        # Perform Scan
        print(f"DEBUG: Scanning path: {final_path}")
        files = scan_directory(final_path)
        print(f"DEBUG: Found {len(files)} files.")
        
        if not files:
             return render_template('index.html', error=f"No PHP files found in: {final_path}")

        results = {}
        for file_path in files:
            print(f"DEBUG: Analyzing {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                results[file_path] = analyze_code(content, file_path)
            except Exception as e:
                results[file_path] = f"Error reading file: {e}"
        
        # Generate Markdown Report String
        report_md = "# Security Analysis Report\n\n"
        for file_path, analysis in results.items():
            report_md += f"## File: `{file_path}`\n\n{analysis}\n\n---\n\n"
            
        # Convert to HTML
        report_html = markdown.markdown(report_md)
        print("DEBUG: Report generated successfully.")
        
        return render_template('report.html', report=report_html, project=project_input)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
