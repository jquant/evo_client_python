import os
import re

def update_test_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add pytest.mark.asyncio import if not present
    if 'import pytest' in content and 'pytest.mark.asyncio' not in content:
        content = content.replace('import pytest', 'import pytest\n\n')
    
    # Update test functions to be async
    content = re.sub(
        r'def (test_[^_\n]*(?:_get|_create|_update|_delete|_cancel|_execute)[^\n]*\([^)]*\)):',
        r'@pytest.mark.asyncio\nasync def \1:',
        content
    )
    
    # Update API calls to use await
    content = re.sub(
        r'(\s+)result = ([^\n]+)api\.([^(\n]+\([^)\n]*async_req=False[^)\n]*\))',
        r'\1result = await \2api.\3',
        content
    )
    content = re.sub(
        r'(\s+)([^\n]+)api\.([^(\n]+\([^)\n]*async_req=False[^)\n]*\))',
        r'\1await \2api.\3',
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    test_dir = 'test/api'
    for filename in os.listdir(test_dir):
        if filename.startswith('test_') and filename.endswith('.py'):
            file_path = os.path.join(test_dir, filename)
            print(f'Updating {file_path}...')
            update_test_file(file_path)

if __name__ == '__main__':
    main() 