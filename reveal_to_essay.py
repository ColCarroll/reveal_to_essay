import os
import subprocess

import click

def get_template():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'template.html'), 'r') as buff:
        return buff.read()

def make_dir(name):
    if not os.path.isdir(name):
        os.mkdir(name)


class WebSkeleton(object):
    thumb_x_px = 300
    thumb_y_px = 225

    def __init__(self, pdf_name, out_dir, force=False):
        self.check_reqs()
        self.pdf_name = pdf_name
        self.out_dir = out_dir
        self.force = force

    def list_sorted_pngs(self, directory):
        """Returns sorted list of pngs in a directory"""
        pngs = []
        for fname in os.listdir(directory):
            if fname.endswith('.png'):
                pngs.append(os.path.join(directory, fname).lstrip(self.out_dir))
        return sorted(pngs)



    def check_reqs(self):
        """Make sure required libraries exist"""
        out = subprocess.run(["which", "pdftoppm"], stdout=subprocess.DEVNULL)
        if out.returncode != 0:
            raise RuntimeError(
                'Install `pdftoppm`, maybe with `brew install poppler`, and try again')

    def normalize_name(self):
        pdf_name = os.path.basename(self.pdf_name)
        if pdf_name.endswith('.pdf'):
            pdf_name = pdf_name[:-4]
        return '_'.join(pdf_name.strip().split())

    def thumbnail_dir(self):
        return os.path.join(self.out_dir, 'thumbs')

    def slide_dir(self):
        return os.path.join(self.out_dir, 'slides')

    def make_thumbnails(self):
        make_dir(self.thumbnail_dir())
        subprocess.run(["pdftoppm",
                        self.pdf_name,
                        os.path.join(self.thumbnail_dir(), self.normalize_name()),
                        "-png",
                        "-scale-to-x",
                        str(self.thumb_x_px),
                        "-scale-to-y",
                        str(self.thumb_y_px)])

    def make_slides(self):
        make_dir(self.slide_dir())
        subprocess.run(["pdftoppm",
                        self.pdf_name,
                        os.path.join(self.slide_dir(), self.normalize_name()),
                        "-png"])

    def build(self):
        if os.path.exists(self.out_dir) and not self.force:
            click.secho(
                "{} already exists!  Cowardly refusing to continue."
                "  Rerun with --force if you want to delete it!".format(self.out_dir))
            return
        make_dir(self.out_dir)
        self.make_thumbnails()
        self.make_slides()
        out_file = os.path.join(self.out_dir, '{}.html'.format(self.normalize_name()))
        html = self.get_html()
        with open(out_file, 'w') as buff:
            buff.write(html)
        click.secho('Template successfully built at {}'.format(out_file))

    def get_html(self):
        template = get_template()
        return template.replace('NOT A HACK', self.get_body())

    def get_body(self):
        tr_template = '''
            <tr>
                <td>
                  <a href="{}">
                    <img src="{}">
                  </a>
                </td>

                <td>
                  <p>FILL
                </td>
            </tr>'''

        thumbs = self.list_sorted_pngs(self.thumbnail_dir())
        slides = self.list_sorted_pngs(self.slide_dir())
        trs = []
        for slide, thumb in zip(slides, thumbs):
            trs.append(tr_template.format(slide, thumb))
        return '\n'.join(trs)


@click.command()
@click.option('--out-dir', '-o', type=click.Path())
@click.option('--pdf-name', '-p', type=click.Path(exists=True, dir_okay=False))
@click.option('--force', '-f', is_flag=True)
def main(out_dir, pdf_name, force):
    WebSkeleton(pdf_name, out_dir, force).build()


if __name__ == '__main__':
    main()
