import os
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # Display a simple form for remote CLI input
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Remote CLI</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                h1 {
                    color: #333;
                    margin-bottom: 20px;
                }
                form {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    display: flex;
                    flex-direction: column;
                    width: 300px;
                    margin-bottom: 20px;
                }
                label {
                    margin-bottom: 10px;
                    font-weight: bold;
                }
                input[type="text"] {
                    padding: 8px;
                    margin-bottom: 15px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                input[type="submit"] {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                pre {
                    background-color: #272c34;
                    color: #fff;
                    padding: 15px;
                    border-radius: 8px;
                    font-family: monospace;
                    width: 90%;
                    max-width: 700px;
                    margin: 0 auto;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                a {
                    margin-top: 20px;
                    color: #007BFF;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Remote CLI</h1>
            <form action="/execute" method="get">
                <label for="command">Enter system command:</label>
                <input type="text" name="command" id="command" placeholder="e.g., ls, whoami, cat /etc/passwd">
                <input type="submit" value="Execute">
            </form>
        </body>
        </html>
    '''

@app.route('/execute')
def execute_command():
    # Get the user input (which is a system command)
    command = request.args.get('command', '').strip()

    if command:
        try:
            # Run the command using subprocess or os.popen
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            result = result.decode('utf-8')  # Decode bytes to string
        except subprocess.CalledProcessError as e:
            result = f"Error executing command: {e}"
    else:
        result = "No command entered."

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Remote CLI - Output</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                h1 {
                    color: #333;
                    margin-bottom: 20px;
                }
                pre {
                    background-color: #272c34;
                    color: #fff;
                    padding: 15px;
                    border-radius: 8px;
                    font-family: monospace;
                    width: 90%;
                    max-width: 700px;
                    margin: 0 auto;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                a {
                    margin-top: 20px;
                    color: #007BFF;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Command Output</h1>
            <pre>{{ result }}</pre>
            <a href="/">Back to CLI</a>
        </body>
        </html>
    ''', result=result)

if __name__ == '__main__':
    app.run(debug=True)
