# created on the 10th of October 2020 by Adrien Leleu
# updated on the 18th of January 2020 by Adrien Leleu 

import numpy as np
import pandas as pd
import csv

# create a single dataframe from all the spreadsheets
df_list1 = pd.read_csv('CHEOPS_authors - CHEOPS_all_papers.csv')
df_list2 = pd.read_csv('CHEOPS_authors - CHEOPS_selected_papers.csv')


# list of people from the CHEOPS_selected_papers.csv
selected_list=['A. Bonfanti',
                'A. Leleu',
                'C.M. Persson',
                'D. Futyan',
                'G. Bou{\'e}', 
                'N. C. Hara', 
                'M. J. Hooton',
                'T. G. Wilson',
                'J.-B. Delisle']


#cret the list of all authors of the paper
df_selected=df_list2[df_list2['author'].isin(selected_list)]
df_list=df_list1.append(df_selected)


all_authors=df_list.author.tolist()



# sort all authors from the spreadsheets in alphabetical order
Family_names=[]
for name in all_authors:
    Family_names.append(name.split('. ')[-1])

Id_sort=sorted(range(len(Family_names)), key=lambda k: Family_names[k])
all_authors_sorted=[all_authors[i] for i in Id_sort]

# write here the authors in the non-alphabetical list, using exactly the same name as in the spreadsheet
authors_nonalpha=['A. Leleu', 'Y. Alibert', 'N. C. Hara', 'M. J. Hooton','T. G. Wilson', 'J.-B. Delisle', 'J. Laskar',
  'S. Hoyer','J. Cabrera','L. Delrez']


# create the author list
authors=authors_nonalpha
for author in all_authors_sorted:
    if author not in authors:
        authors.append(author)

    
institutes=[]
authors_institutes=[]
acknowledgements=[]
institutes_Id=[]

for author in authors:
    print('author',author)
    
    author_insistutes_f=df_list[df_list['author']==author]
    
    
    #institute list
    author_institutes_list=author_insistutes_f.values.tolist()[0][3:7]
    author_institutes_fnn = [x for x in author_institutes_list if str(x) != 'nan']
   
    author_institutes=[]
    for institute in author_institutes_fnn:
        # if the institute is already in the list, add its index next to the author name
        if institute in institutes: 
            author_institutes.append(institutes.index(institute))
        #if not, create a new entry in the institute list
        else:
            institutes.append(institute)
            author_institutes.append(institutes.index(institute))
    authors_institutes.append(author_institutes)
    
    #acknowledgments list following the order of the author list
    author_acknow_list=author_insistutes_f.values.tolist()[0][7:11]
    
    author_acknow_fnn = [x for x in author_acknow_list if str(x) != 'nan'] 
    for acknow in author_acknow_fnn:
        if acknow not in acknowledgements:
            acknowledgements.append(acknow)
            
#print(authors_institutes)
#print(institutes)


# write the author list, with the institutes indexes, on a column
outF = open("authors.txt", "w")
for l,line in zip(range(len(authors)),authors):
  line_str=authors[l]+"$^{"
  if len(authors_institutes[l])==0:
      line_str+=str(0)+","
  else:
      for k in range(len(authors_institutes[l])):
          line_str+=str(authors_institutes[l][k]+1)+","
  line_str=line_str[:-1]+"}$, "
  outF.writelines(line_str)
  outF.write("\n")

outF.close()


# write the author list, with the institutes indexes, in a line
outF = open("authors_lin.txt", "w")
for l,line in zip(range(len(authors)),authors):
  outF.writelines(line+", ")

outF.close()


# write the institute list
outF = open("institutes.txt", "w")
for l,line in zip(range(len(institutes)),institutes):
  line_str="$^{"+str(l+1)+"}$ "+line.rstrip()+"\\\\"
  outF.writelines(line_str)
  outF.write("\n")

outF.close()


# write the acknowledgement list
outF = open("acknowledgements.txt", "w")
for l,line in zip(range(len(acknowledgements)),acknowledgements):
  toprint=line.rstrip()
  if toprint[-1]=='.':
      outF.writelines(line.rstrip()+" ")
  else:
      outF.writelines(line.rstrip()+". ")
  outF.write("\n")

outF.close()


