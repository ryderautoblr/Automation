# run this in any directory 
# add -v for verbose 
# get Pillow (fork of PIL) from 
# pip before running --> 
# pip install Pillow 

# import required libraries 
import os 
import sys 
from PIL import Image 
import shutil

# define a function for 
# compressing an image 
def compressMe(path,file, newPath, verbose = False,_quality=90): 
    
    # open the image 
    picture = Image.open(path + "\\" + file) 
    
    # Save the picture with desired quality 
    # To change the quality of image, 
    # set the quality variable at 
    # your desired level, The more 
    # the value of quality variable 
    # and lesser the compression
    newFile =  newPath + "\\Compressed_"+file
    picture.save(newFile, 
                "JPEG", 
                optimize = True, 
                quality = _quality) 
    size = os.path.getsize(newFile)
    return size

# Define a main function 
def main(): 
    
    verbose = False
    
    # checks for verbose flag 
    if (len(sys.argv)>1): 
        
        if (sys.argv[1].lower()=="-v"): 
            verbose = True
                    
    # finds current working dir 
    cwd = "D:\\Studds Images Compress\\MULTI IMAGE BANK\\SLOT-2\\" 
    outputPath = "D:\\Studds Images Compress\\MULTI IMAGE BANK COMPRESSED\\SLOT-2\\" 

    maxSize = 0
    maxCompressSize = 0
    minSize = 1e9
    minCompressSize = 1e9
    for (dirpath, dirnames, filenames) in os.walk(cwd):
        for d in dirnames:
            for (dirpath1,dirnames1,f1) in os.walk(cwd+d):
                newPath = outputPath + d
                try:  
                    os.mkdir(newPath)  
                except OSError as error:  
                    #print(error)
                    x=1
    
                for f in f1:
                    file = dirpath1+"\\"+f
                    size = os.path.getsize(file)
                    
                    maxSize = max(size,maxSize)
                    minSize = min(size,minSize)
                    if size > (6.5*1e6):
                        compressSize = compressMe(dirpath1, f, newPath, verbose)
                        # print (f)
                    else:
                        compressSize = size
                        shutil.copy(dirpath1 + "\\" + f,newPath + "\\Compressed_"+f)

                    maxCompressSize = max(compressSize,maxCompressSize)
                    minCompressSize = min(compressSize,minCompressSize)
                    print ("Done: ",f)

    print(maxSize/1e6,maxCompressSize/1e6)
    print(minSize/1e6,minCompressSize/1e6)

    print("Done") 

# Driver code 
if __name__ == "__main__": 
    main() 
