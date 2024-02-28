###################################################################
# Computer Project #9
# Read the image data from the JSON file
# Put the data into a master dictionary of dictionaries 
# Create a list of the category names and captions  
# Display the mapping of each category based on the list of images
# Prompt the user for image category options 
# Display the max and min of occurences of an object
# Display closing messages
###################################################################

import json
import string

STOP_WORDS = ['a','an','the','in','on','of','is','was','am','I','me','you',\
 'and','or','not','this','that','to','with','his','hers','out','it','as','by',\
     'are','he','her','at','its']

MENU = '''
    Select from the menu:
        c: display categories
        f: find images by category
        i: find max instances of categories
        m: find max number of images of categories
        w: display the top ten words in captions
        q: quit
        
    Choice: '''
OPTIONS = "cfimwq"

def get_option():
   """
       Prompts the user for a valid option and returns it as a string
       None
       Returns: Lower case string 
   """
   while True:
       #bring up the menu option to select from
       menu_option=input(MENU)
       #lower the leter entered by user
       menu_option=menu_option.lower()
       #look for the letter in OPTIONS to see if it exists
       for x in OPTIONS:
           #if the letter does exist, follow through loop
           if menu_option == x:
               #return the letter entered
               return menu_option
       #entered value was not one of the options, print error message
       print ("Incorrect choice.  Please try again.")
       
def open_file(s):
   """
       Prompts the user for the name of the input file and after opens it
       Value: A string 
       Returns: The pointer
   """
   while True: 
       #prompt user to input a filename
       filename= input ("Enter a {} file name: ".format(s))
       try:
           #open the file printed and make sure it is the correct title
           fp= open (filename)
           break
       #for invalid file names, print error and ask user again
       except FileNotFoundError:
           print ("File not found.  Try again.")
           continue
   #return the new file 
   return fp
        
def read_annot_file(fp1):
   """
       Read the JSON file
       Value: File pointer
       Returns: Dictionary of dictionaries (DD)
   """
   #load the json file
   D=json.load(fp1) #dictionary
   #return the dictionary
   return D

def read_category_file(fp2):
   """
       Create a dictionary whose key is the int and whose value is the string
       Value: File pointer
       Returns: A dictionary (D)
   """
   catD = dict() #dictionary
   #check each line in the fp2 file
   for line in fp2:
       #remove the spaces between each key and value
       l=line.split()
       #test for no more items in the list
       if len(l) > 1:
           #update the dictionary with no spaces 
           catD.update({int(l[0]): l[1]})
   #return the new dictionary
   return catD

def collect_catogory_set(D_annot,D_cat):
   """
       Print the category names (strings)
       Value: dictionary of dictionaries (DD), dictionary (D)
       Returns: A set of strings (sett)
   """
   #create a set
   sett=set() #set
   #create a list based off of the set
   settList=[]
   #go through each item in the dict
   for key,value in D_annot.items():
       #getting the list of category numbers
       clist=value.get("bbox_category_label")
       for x in clist:
           if x in D_cat:
               s = D_cat.get(x)
               if s not in settList:
                   settList.append(s)
   #convert the list to a set
   sett.update(settList)
   #return the set
   return sett
           
          
def collect_img_list_for_categories(D_annot,D_cat,cat_set):
   """
       Create a mapping of each category to the list of images that has an
       instance of that category
       Value: dictionary of dictionaries (DD), dictionary (D), set of strings \
           (sett)
       Returns: Dictionary of sorted lists ()
   """
   imgD = dict() #dictionary
   settList=[] #set list
   for x in cat_set:
       #create a list as a placeholder for each category name in the dictionary
       imgD.update({x: list()})
   #go through each item in the D_annot
   for key,value in D_annot.items():
       #clear the set list through each loop
       settList.clear()
       #getting the list of category numbers
       clist=value.get("bbox_category_label")
       for x in clist:
            if x in D_cat:
                s = D_cat.get(x)
                #grab the image list for that category
                imgList = imgD.get(s)
                #if this key is already in image list then continue
                # if key in imgList:
                #     continue
                #append the image to the image settList
                imgList.append(key)
                #sort the list
                imgList.sort()
                #update the dictionary
                imgD.update({s: imgList.copy()})
   return imgD

def max_instances_for_item(D_image):
   """
       Finds the most occurrences of an object across all images
       Value: Dictionary of sorted lists (DD)
       Returns: A tuple (max_list)
   """
   #create a list for the max value
   mcat=[0,""]  
   #look through the list of items found in the picture
   for key, value in D_image.items():
        if len(value) > mcat[0]:
            mcat[0] = len(value)
            mcat[1] = key
   return(tuple(mcat))

def max_images_for_item(D_image):
   """
       Finds the most images that an object appears in
       Value: Dictionary of sorted lists (DD)
       Returns: A tuple (mcat)
   """
   mcat = [0,""] #max category item
   for key, value in D_image.items():
       #transform value list into a set
       value_set = set(value)
       if len(value_set) > mcat[0]:
           mcat[0] = len(value_set)
           mcat[1] = key
   #return the tuple version of mcat
   return(tuple(mcat))

def count_words(D_annot):
   """
       Counts the occurrences of words in captions
       Value: Dictionary of dictionaries (DD)
       Returns: List of tuples (tuple_list)
   """
   tempD = dict()
   word_list = []
   count_list_list = []
   tuple_list = []
   for key, value in D_annot.items():
       clist = value.get("cap_list")
       for x in clist:
           #remove punctuation
           for ele in x:
               if ele in string.punctuation:
                   x = x.replace(ele, "")
           # divide words in sentence into a list of words
           word_list = x.split()
           for word in word_list:
               if word not in STOP_WORDS: #don't include words in stop list
                   if word not in tempD:
                       tempD.update({word: int(1)}) #add first item to dict
                   else:
                       tempD.update({word: tempD.get(word) + 1})
   #transform into list of tuples
   for key, value in tempD.items():
       count_list_list.append(list( (value,key) ))
   #sort by number then string
   count_list_list.sort(key=lambda row: (row[0], row[1]),reverse = True)
   #convert to tuple list
   for item in count_list_list:
       tuple_list.append(tuple(item))
   return(tuple_list)

def main():    
    print("Images\n")
    # open the file of the JSON image
    fp=open_file("JSON image")
    dd = read_annot_file(fp)
    #open the category file
    fp2 = open_file("category")
    rd = read_category_file(fp2) #read category file
    ccs = collect_catogory_set(dd, rd) #collect catogory set
    cil = collect_img_list_for_categories(dd, rd, ccs) #collect img list
    #go through the options that the user could enter
    while True:
        sel = get_option() #selection
        #if the user enters q , end the program
        if sel=='q': break
        #if the user enters c, display the categories
        if sel == 'c':
            clist = list(ccs)
            clist.sort()
            print("Categories:")
            #seperate by commas
            print(", ".join(clist))
            continue
        #if the user enters f, find the images by category
        if sel == 'f':
            clist = list(ccs)
            #sort the list
            clist.sort()
            print("Categories:")
            #seperate by commas
            print(", ".join(clist))
            while True:
                #determine if what the user entered is valid
                c = input("Choose a category from the list above: ")
                if c not in clist:
                    print("Incorrect category choice.")
                    continue
                print("The category {} appears in the following images:"\
                      .format(c))
                #pull out image info for category chosen
                ilist = cil.get(c)
                #transform to a set to removed redundant image ids
                iset = set(ilist)
                #transform back to list so numbers can be sorted
                ilist = list(iset)
                #convert to integers
                for i in range(0,len(ilist)):
                    ilist[i] = int(ilist[i])
                #sort integer list low-to-high
                ilist.sort()
                print(", ".join(str(e) for e in ilist))
                break
            continue
        #if user enters i, find the max instances of categories and display
        if sel == 'i':
            maxi = max_instances_for_item(cil) #max instances for item
            print("Max Instances: the category {} appears {} times in images."\
                  .format(maxi[1],maxi[0]))
            continue
        #if user enters m, find and display the max number of img in category
        if sel == 'm':
            mif = max_images_for_item(cil) #max images for item
            print("Max images: the category {} appears in {} images."\
                  .format(mif[1],mif[0]))
            continue
        #if user enters w, display the top ten words 
        if sel == 'w':
            count_w = count_words(dd) #count words
            inpt = input("Enter number of desired words: ")
            #test for valid input
            if inpt.isalnum():
                continue
            print("Top {} words in captions.".format(int(inpt)))
            print("{:<14s}{:>6s}".format("word","count")) 
            for num in range(0,int(inpt)):
                print("{:<14s}{:>6d}".format(count_w[num][1],count_w[num][0]))
            continue
    print("\nThank you for running my code.")
    
    
# Calls main() if this modules is called by name
if __name__ == "__main__":
    main()     
