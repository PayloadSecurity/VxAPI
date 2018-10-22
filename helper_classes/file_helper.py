import os


class FileHelper:

    @staticmethod
    def get_file_from_dir_recursively(path):
        retrieved_files = []
        for folder, subs, files in os.walk(path):
            for filename in files:
                retrieved_files.append(os.path.join(folder, filename))

        return retrieved_files

