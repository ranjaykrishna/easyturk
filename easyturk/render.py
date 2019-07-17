"""Script to render a given EasyTurk task.
"""

import argparse

from easyturk import EasyTurk


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    # Compile the template.
    et = EasyTurk()
    env = et.get_jinja_env()
    template = env.get_template(args.template)

    html = template.render({'input': ''})

    # Save to output.
    with open(args.output, 'w') as f:
        f.write(html)
