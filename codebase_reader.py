import os, subprocess, tempfile
from urllib.parse import urljoin

def get_files(target_root, target_extensions):
    target_files = []
    for root, dirs, files in os.walk(os.path.join(target_root)):
        for file in files:
            if any(file.endswith(target_extenstion) for target_extenstion in target_extensions):
                target_files.append(os.path.join(root, file))
    return target_files

def get_extensions(target_root):
    extensions = set()
    for root, dirs, files in os.walk(target_root):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                extensions.add(ext)
    return list(extensions)

def get_codebase_text(target_root, target_extensions):
    codebase_text = ''
    for filename in get_files(target_root, target_extensions):
        # with open(filename, 'r', encoding='utf-8') as file:
        with open(filename, 'r', encoding='iso-8859-1') as file:
            codebase_text += f'# {os.path.basename(filename)}\n\n'
            codebase_text += file.read()
            codebase_text += '\n\n---------------------\n\n'
    return codebase_text

def get_codebase_from_github(repo, target_extensions):

    with tempfile.TemporaryDirectory() as tmp_dir:
        url = urljoin('https://github.com/', repo)
        cmd = ['git', 'clone', url, tmp_dir]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Error cloning repository. stderr: {stderr.decode()}, stdout: {stdout.decode()}")

        # print(f"Repository cloned successfully at {tmp_dir}")
        
        codebase_text = get_codebase_text(tmp_dir, target_extensions)
        return codebase_text
    
if __name__ == '__main__':
    # print(get_files('.', ['.py']))
    # print(get_extensions('.'))
    # print(get_codebase_text('.'))
    text = get_codebase_from_github('hwchase17/langchain', ['.py'])
    print(text)

    