import os


def read_first_line(fname):
    """
    Read fist line of file
    :param filename:
    :return:
    """
    data =[]
    with open(fname, "r") as data_file:
        line = data_file.readline()
        data = line.strip().split()
    return data  
    

def main(fname):
  statinfo = os.stat(fname)
  size = int(statinfo.st_size)
  
  #assert less than 100 gigabytes
  assert size<1e9
  
  column_num = len(read_first_line(fname))
  
  
  
  
