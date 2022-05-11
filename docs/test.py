import subprocess
import tempfile

with tempfile.TemporaryFile() as tempf:
    proc = subprocess.Popen(['echo', 'a', 'b'], stdout=tempf)
    proc.wait()
    tempf.seek(0)
    print(tempf.read())