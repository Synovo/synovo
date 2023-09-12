import os
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
    
    for i in files:
        if type(i) is str:
            final_dest = template_utils.map_source_to_dest(root, build, i)[0]
            
            localised = [i for i in final_dest[len(build):].split('/') if len(i.strip()) > 0]
            
            if localised[0] in languages:
                i = '/'.join(localised[1:])
                
                if i in documents:
                    documents[i].append(localised[0])
                else:
                    documents[i] = [localised[0]]
            else:
                print("Invalid page name: {}".format(i), file=sys.stderr)
                continue
    
    for i, languages in documents.items():
        if type(i) is str:
            out.append('<a href="{dest}">{text}</a>'.format(dest=os.path.join('/' + (lang if lang in languages else languages[0]), i), text=i.split('/')[-1]))
        elif type(i) is list:
            out.append('<div class="indent"><label>{}</label>{nested}</div>'.format(nested=to_html_nav(root, i, build, languages)))
            
    return '<nav>{}</nav>'.format(''.join(out))

def get_nav(source, current_language, build, languages):
    return to_html_nav(source, getFiles(source), build, current_language, languages)
