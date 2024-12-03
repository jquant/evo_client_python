import os
import glob

def combine_markdown_files():
    # Get all .md files from the docs directory
    md_files = glob.glob('docs/*.md')
    
    # Filter out files containing 'viewmodel' (case insensitive)
    filtered_files = [f for f in md_files if 'viewmodel' not in f.lower()]
    
    # Sort files to ensure consistent ordering
    filtered_files.sort()
    
    # Create the combined markdown file
    with open('combined_docs.md', 'w', encoding='utf-8') as outfile:
        # Add a title to the combined file
        outfile.write('# Combined API Documentation\n\n')
        
        for filename in filtered_files:
            # Add a section divider and the filename as a header
            outfile.write(f'\n## {os.path.basename(filename)[:-3]}\n\n')
            
            # Read and write the contents of each file
            with open(filename, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n\n---\n')  # Add a horizontal rule between files

if __name__ == '__main__':
    combine_markdown_files()
    print("Documentation has been combined into 'combined_docs.md'") 