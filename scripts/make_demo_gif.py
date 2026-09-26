"""Render actual offline CLI output with Pillow; no terminal recorder needed."""
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont
from run_demo import ROOT, run_demo


def main() -> None:
    font = ImageFont.load_default(size=18)
    frames = []
    for command, output in run_demo():
        if ' checklist ' in ' ' + command + ' ':
            record = json.loads(output)
            output = json.dumps({'done': record['done'], 'total': record['total']}, indent=2)
            output += '\nFull CLI output includes each item, citation and status.'
        lines = textwrap.wrap('$ ' + command, width=90)
        for line in output.splitlines():
            lines.extend(textwrap.wrap(line, width=90, replace_whitespace=False) or [''])
        image = Image.new('RGB', (1060, 700), '#0f2030')
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((16, 16, 1044, 65), radius=10, fill='#24374d')
        draw.text((32, 29), 'TCPA TOOLKIT | offline demo | fictional numbers', font=font, fill='#93e7ca')
        for index, line in enumerate(lines):
            draw.text((30, 90 + index * 24), line, font=font,
                      fill='#93e7ca' if index < len(textwrap.wrap('$ ' + command, width=90)) else '#eef3f8')
        draw.text((30, 658), 'Operational checks only. Not legal advice.', font=font, fill='#b9c9de')
        frames.append(image)
    target = ROOT / 'docs/demo.gif'
    frames[0].save(target, save_all=True, append_images=frames[1:], duration=2400, loop=0, optimize=True)
    print(f'Generated {target.relative_to(ROOT)} ({target.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
