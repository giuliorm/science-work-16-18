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

def get_path(dir, file_path):
    filename = re.search("\\\([0-9]+_?[0-9]*\.fbx$)", file_path)
    fn = None
    if filename is not None:
        fn = filename.group().replace(".fbx", ".csv")
    return "{0}{1}".format(dir, fn)

def get_data(file_path):
    mapper = FbxMapper(file_path)
    mapper.FbxToData()
    return mapper.filter()

def toCSV(names, data):
    result = toCSVLine(names)
    format = "{0}\n{1}"
    for row in data:
        result = format.format(result, toCSVLine(row))
    return result

def dataToCSV(path, names, data):
    f = open(path, "w")
    f.write(toCSVLine(names, "%s"))
    #format = "{0}\n{1}"
    for row in data:
        f.write(toCSVLine(row, "%.5f"))
        #result = format.format(result, toCSVLine(row))
    f.close()

def toCSVLine(data, format):
  s = ','.join(format % d for d in data)
  return "{0}\n".format(s)

if __name__ == "__main__":
    fbx_dir_path = "C:\Users\ZotovYul\Documents\New Unity Project\Assets\Huge Mocap Library\mocap animations"
    fbx_files = findfiles(fbx_dir_path)
    mapper = FbxMapper(fbx_files[0])
    mapper.FbxToData()
    names, data = mapper.filter()
    dataToCSV(get_path("C:\Temp\\", fbx_files[0]), names, data)
    exit(-1)
    # sc = SparkContext(appName="FbxSpark")
    # fbx_files = sc.parallelize(fbx_files)
    # new_paths = {}
    # for file in fbx_files:
    #     new_paths[file] = get_path(file)
    #
    # fbx_files\
    #     .map(get_data)\
    #     .map(lambda names, data: toCSV(names, data))\

    # counter = sc.parallelize((1,2,3,4))
    # for c in counter.collect():
    #    print("%d " % c)

    sc.stop()