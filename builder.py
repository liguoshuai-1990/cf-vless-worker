import json
import base64
import os

def obfuscate_string(s):
    # Base64 encode the string and wrap it in atob()
    b64 = base64.b64encode(s.encode()).decode()
    return f"atob('{b64}')"

def build():
    # Use absolute paths
    base_dir = "/home/zrlgs/.openclaw/workspace/cf-vless-worker-clone"
    
    with open(os.path.join(base_dir, 'config.json'), 'r') as f:
        config = json.load(f)
    
    with open(os.path.join(base_dir, 'dist/_worker.js'), 'r') as f:
        content = f.read()

    # Obfuscate userID
    # Original: let userID = "4316fe33-e607-47b1-8c29-60f585cf630e";
    # We want: let userID = atob('...');
    # Note: Using replace might match multiple places if userID is used as a string.
    # Be careful.
    
    # We can use a regex or specific replacement for the variable declaration
    import re
    content = re.sub(r'let userID = ".*?";', f'let userID = {obfuscate_string(config["uuid"])};', content)
    
    with open(os.path.join(base_dir, 'dist/_worker.js'), 'w') as f:
        f.write(content)
    
    print("Obfuscation complete.")

if __name__ == '__main__':
    build()
