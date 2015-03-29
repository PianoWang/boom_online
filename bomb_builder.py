import os
import time


# TODO automatically delete the temporary files
def build_bomb(path, username):
    old_wd = os.getcwd()
    os.chdir(path)
    key = int(time.time())
    source_writer_fp = None
    proto_source_fp = None
    header_writer_fp = None
    try:
        source_name = str.format("{0}.c", username)
        header_name = str.format("{0}.h", username)
        os.system('touch '+source_name)
        os.system('touch '+header_name)
        source_writer_fp = open(source_name, 'w')
        header_writer_fp = open(header_name, 'w')
        proto_source_fp = open('prototype.c', 'r')
        header_writer_fp.write(str.format('int key = {0};\n', key))
        source_writer_fp.write(str.format('#include "{0}"\n', header_name))
        source = proto_source_fp.read()
        source_writer_fp.write(source)
    finally:
        if source_writer_fp:
            source_writer_fp.close()
        if proto_source_fp:
            proto_source_fp.close()
        if header_writer_fp:
            header_writer_fp.close()
    os.chdir(old_wd)