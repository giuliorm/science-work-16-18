from pyspark import SparkContext
import os, re
from fbx_mapper.fbx_mapper import FbxMapper

def findfiles(directory):
    objects = os.listdir(directory)  # find all objects in a dir
    files = []
    for i in objects:  # check if very object in the folder ...
        path = os.path.join(directory, i).replace('\'', '')
        if isFile(path):  # ... is a file.
            if re.search("\.fbx$", path) is not None:
                files.append(path)  # if yes, append it.
        else:
            files.extend(findfiles(path))
    return files


def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True


if __name__ == "__main__":
    fbx_dir_path = "C:\Users\ZotovYul\Documents\New Unity Project\Assets\Huge Mocap Library\mocap animations"
    fbx_files = findfiles(fbx_dir_path)

    mapper = FbxMapper(fbx_files[0])
    names, data = mapper.FbxToData()
    mapper.DataToCsv("C:\Temp\csv_temp.csv")
    exit(-1)
    sc = SparkContext(appName="FbxSpark")
    fbx_files = sc.parallelize(fbx_files)
    fbx_files.map(lambda file: file)
    # counter = sc.parallelize((1,2,3,4))
    # for c in counter.collect():
    #    print("%d " % c)

    sc.stop()