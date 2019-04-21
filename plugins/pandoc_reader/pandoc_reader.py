import subprocess
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open
import frontmatter


class PandocReader(BaseReader):
    enabled = True
    file_extensions = ['md', 'markdown', 'mkd', 'mdown']

    def read(self, filename):
        with pelican_open(filename) as fp:
            metadata, content = frontmatter.parse(fp)

        # date is parsed as datetime object, convert back to string
        if metadata.get("date"):
            metadata["date"] = metadata["date"].strftime("%Y-%m-%d")
        
        # tags and authors must be comma-separated lists for pelican
        for x in ("tags", "authors"):
            if isinstance(metadata.get(x), list):
                metadata[x] = ", ".join(metadata[x])

        extra_args = self.settings.get('PANDOC_ARGS', [])
        extensions = self.settings.get('PANDOC_EXTENSIONS', '')

        if "bibliography" in metadata and PANDOC_CSL:
            extensions + ['--filter',
                          'pandoc-citeproc',
                          '--bibliography',
                          './bib/' + metadata["bibliography"],
                          '--csl',
                          PANDOC_CSL]

        if isinstance(extensions, list):
            extensions = ''.join(extensions)

        pandoc_cmd = ["pandoc", "--from=markdown" + extensions, "--to=html5"]
        pandoc_cmd.extend(extra_args)


        # final processing of metadata via Pelican
        for key, val in metadata.items():
            metadata[key] = self.process_metadata(key, val)

        # final processing of content via pandoc
        proc = subprocess.Popen(pandoc_cmd,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)

        output = proc.communicate(content.encode('utf-8'))[0].decode('utf-8')
        status = proc.wait()
        if status:
            raise subprocess.CalledProcessError(status, pandoc_cmd)

        # TG: fix for broken {filename} past pandoc 1.15
        output = output.replace('%7Bfilename%7D', '{filename}')
        return output, metadata


def add_reader(readers):
    for ext in PandocReader.file_extensions:
        readers.reader_classes[ext] = PandocReader


def register():
    signals.readers_init.connect(add_reader)
