import os
import re
import sys
import template_utils

def getFiles(path=os.curdir):
    files = []
    if os.path.isfile(path):
        files.append(path)
        return files
    
    for item in os.listdir(path):
        item = os.path.join(path, item)
        
        if os.path.isfile(item):
            files.append(item)
                
        else:
            tmp = getFiles(item)
            if len(tmp) > 0:
                files.append(tmp)
            
    return files

def to_html_nav(root, files, build, lang, languages):
    out = []
    
    documents = {}
    document_titles = {}
    
    for file_name in files:
        if type(file_name) is str:
            final_dest = template_utils.map_source_to_dest(root, build, file_name)[0]
            
            localised = [i for i in final_dest[len(build):].split('/') if len(i.strip()) > 0]
            
            if localised[0] in languages:      
                localised_file = '/'.join(localised[1:])
                
                with open(os.path.join(root, file_name), 'r') as file:
                    title = re.search(r"<h[1-6]>([^<]*)</h[1-6]>", file.read())
                    
                    if title is not None:
                        document_titles[localised_file] = title.group(1).capitalize()
                    else:
                        document_titles[localised_file] = ' '.join(final_dest.split('/')[-1].split('.')[:-1]).capitalize()
                
                if localised_file in documents:
                    documents[localised_file].append(localised[0])
                else:
                    documents[localised_file] = [localised[0]]
            else:
                print("Invalid page name: {}".format(final_dest), file=sys.stderr)
                continue
        else:
            out.append('<div class="indent"><label>{text}</label>{nested}</div>'.format(text=file_name[0].split('/')[-2].capitalize(), nested=to_html_nav(root, file_name, build, lang, languages)))
    
    for i, languages in documents.items():
        out.append('<a href="{dest}">{text}</a>'.format(dest=os.path.join('/' + (lang if lang in languages else languages[0]), i), text=document_titles[i]))
            
    return '<nav>{}</nav>'.format(''.join(out))

def get_nav(source, current_language, build, languages):
    
    return to_html_nav(source, getFiles(source), build, current_language, languages)
