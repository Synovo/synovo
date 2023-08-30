import os
import template_utils

def template(file):
    with open(file, 'r') as html:
        data = html.read()

        with open(os.path.abspath('./template.html'), 'r') as file:
            template = file.read()
            file.close()

        while '<?py(' in template:
            block = template.index('<?py(')
            end = template.index(')?>', block)

            python = template[block + 5:end]

            template = template[:block] + str(eval(python, { k: getattr(template_utils, k) for k in dir(template_utils) if not k.startswith('_') }, {
                'file': file,
                'body': data
            })) + template[end + 3:]

        while '<?py{' in template:
            block = template.index('<?py{')
            end = template.index('}?>')

            python = template[block + 5:end]

            exec(python, { k: getattr(template_utils, k) for k in dir(template_utils) if not k.startswith('_') }, {
                'file': file,
                'body': data
            })

            template = template[:block] + template[end + 3:]

        html.close()
        return template

def escape(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')
