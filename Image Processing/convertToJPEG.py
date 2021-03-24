import os 
import sys 
from PIL import Image 
import shutil

# define a function for 
# compressing an image 
def convertMe(path,file, newPath, verbose = False): 
    
    # open the image 
    picture = Image.open(path + "\\" + file) 
    
    if '.png' in file: 
        bg = Image.new("RGB", picture.size, (255,255,255))
        bg.paste(picture,picture)
        picture = bg

    newFile =  newPath + "\\Converted_"+file.split('.')[0] + '.JPEG'
    picture.save(newFile, 
                "JPEG") 


# Define a main function 
def main(): 
    
    # finds current working dir 
    cwd = "D:\\Mavox\\Images\\" 
    outputPath = "D:\\Mavox\\Images Converted\\" 

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
                    print ("Start: ",f)
                    file = dirpath1+"\\"+f
                    if ('.db' not in f) and ('.psd' not in f) :
                        convertMe(dirpath1, f, newPath)
                    
                    print ("Done: ",f)

    print("Done") 

# Driver code 
if __name__ == "__main__": 
    main() 
