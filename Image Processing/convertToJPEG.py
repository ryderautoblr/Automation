import os 
import sys 
from PIL import Image 
import shutil
import sys
sys.path.insert(1,"../pathInit/")
import pathInit

# define a function for 
# compressing an image 
def convertMe(path,file, newPath, verbose = False): 
    
    # open the image 
    picture = Image.open(path + "\\" + file) 
    
    if '.png' in file: 
        bg = Image.new("RGB", picture.size, (255,255,255))
        bg.paste(picture,picture)
        picture = bg

    newFile =  newPath + "\\"+file.split('.')[0] + '.JPEG'
    picture.save(newFile, 
                "JPEG") 


# Define a main function 
def main(): 
    
    # finds current working dir 
    cwd = "C:\\Users\\umesh\\OneDrive\\Images\\Aaron\\HELMET EDITED\\" 
    outputPath = "C:\\Users\\umesh\\OneDrive\\Images\\Aaron\\HELMET EDITED CONVERTED\\" 

    files = pathInit.getAllFiles(cwd)
    print (len(files))
    for f in files:
        path, name = os.path.split(f)
        newPath = path.replace(cwd,outputPath)
        try:  
            os.makedirs(newPath)
        except OSError as error:
            pass

        print ("Start: ",f)
        if ('.db' not in f) and ('.psd' not in f) :
            convertMe(path, name, newPath)
        
            print ("Done: ",f)
    print("Done") 

# Driver code 
if __name__ == "__main__": 
    main() 
