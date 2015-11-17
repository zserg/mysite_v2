import subprocess
import tempfile

def input_via_editor(editor):
        """Launch editor on an empty temporary file, wait for it to exit, and
        if it exited successfully, return the contents of the file.

         """
         with tempfile.NamedTemporaryFile() as f:
            f.close()
         try:
            subprocess.check_call([editor, f.name])
         except subprocess.CalledProcessError as e:
            raise IOError("{} exited with code {}.".format(editor, e.returncode))
         with open(f.name) as g:
            return g.read()
