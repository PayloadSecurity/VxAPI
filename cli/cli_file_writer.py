import os
from io import BytesIO
import gzip
import errno
from exceptions import FailedFileSavingError


class CliFileWriter:

    @staticmethod
    def write(dir_path, filename, content):
        CliFileWriter.create_dir_if_not_exists(dir_path)
        retrieved_filename_without_gz_ext, retrieved_file_extension = os.path.splitext(filename)

        mode = 'wb' if type(content).__name__ == 'bytes' else 'w'
        f_out_name = dir_path

        if retrieved_file_extension == '.gz':
            f_out_name += '/' + retrieved_filename_without_gz_ext  # As we want to unpack it, put filename without '.gz. extension
            f_out = open(f_out_name, mode)
            try:
                gzip_file_handle = gzip.GzipFile(fileobj=BytesIO(content))
                f_out.write(gzip_file_handle.read())
            except Exception as e:
                f_out_name += retrieved_file_extension
                f_out = open(f_out_name, mode)
                f_out.write(content)
                f_out.close()
            f_out.close()
        else:
            f_out_name += '/' + filename
            f_out = open(f_out_name, mode)
            f_out.write(content)
            f_out.close()

        return f_out_name

    @staticmethod
    def create_dir_if_not_exists(dir_path):
        if os.path.exists(dir_path):
            if not os.path.isdir(dir_path):
                raise FailedFileSavingError('Given output path \'{}\' points a file instead of directory.'.format(dir_path))
        else:
            try:
                os.makedirs(dir_path)
            except OSError as exc:
                if exc.errno == errno.EACCES:
                    raise FailedFileSavingError('Failed to create directory in \'{}\'. Possibly it\'s connected with file rights.'.format(dir_path))
                else:
                    raise
