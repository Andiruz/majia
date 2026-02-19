import sys
from pathlib import Path
from mako.lookup import TemplateLookup


def render_template(template_path, lookup):
    """
    Render a Mako template (.mako) without external context
    and write the output file without the .mako extension.
    """
    template_path = Path(template_path)

    if template_path.suffix != ".mako":
        raise ValueError("Template file must have a .mako extension")

    output_path = template_path.with_suffix("")
    template = lookup.get_template(template_path.name)
    rendered_content = template.render()
    output_path.write_text(rendered_content, encoding="utf-8")

    print(f"Rendered file written to: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: majia file1.mako [file2.mako ...]")
        sys.exit(1)

    template_paths = [Path(p) for p in sys.argv[1:]]
    directories = sorted({str(p.parent) for p in template_paths})
    lookup = TemplateLookup(directories=directories)

    for path in template_paths:
        try:
            render_template(path, lookup)
        except Exception as e:
            print(f"Error rendering {path}: {e}", file=sys.stderr)
