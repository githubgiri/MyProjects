#Code to match a JD and pull out matching profiles basedonamndatory skillset, 
#additional skills and years of experience

import nltk
import io
import os
import sys
import pandas as pd
from nltk.corpus import stopwords
from nltk.tag import pos_tag
keywords_dict={}
JD_dict={}
score_dict={}
synonyms = []
mand_keywords = []
mand_skillset = []
pref_list2=[]

'''import sys 
reload(sys)
sys.setdefaultencoding("utf-8")'''


#1 : Mandatory skills fetch
#Using the mand words list, fetch the lines in JD that have the mandatory skills defined and tokenize them
mand=['mandatory','compulsory','necessary','required','must have']
mand_list = []
jd_file=sys.argv[1]

for keyword in set(mand):
    mand_list.append([line for line in open(jd_file) if keyword in line.lower()])
    mand_list_1=    [val for d in mand_list for val in d]
mand_list_str = ' '.join(mand_list_1)
tokens = nltk.word_tokenize(mand_list_str)
stopword = set(stopwords.words('english'))
mand_keywords = list(set(tokens).difference(stopword))
mand_tag=pos_tag(mand_keywords)
mand_skillset=[word for word,pos in mand_tag if pos=='NNP']


#2 : Preferred Skillset
pref_list = ['plus','added','additional','preferred','optional']
for keyword in set(pref_list):
    pref_list2.append([line for line in open(jd_file) if keyword in line.lower()])
    pref_list_1=    [val for d in pref_list2 for val in d]
pref_list_str = ' '.join(pref_list_1)
tokens = nltk.word_tokenize(pref_list_str)
stopword = set(stopwords.words('english'))
pref_keywords = list(set(tokens).difference(stopword))
pref_tag=pos_tag(pref_keywords)
pref_skillset=[word for word,pos in pref_tag if pos=='NNP']


#3 : Years of Experience fetching
filecontent=open(jd_file).read()
before, term, after = filecontent.partition('years')
expstr=before.replace("+", " ")
exp1=[int(s) for s in expstr.split() if s.isdigit()]
if not exp1:
    exp_yop=0
else:
    exp_yop=exp1[-1]
total_profiles=0
yop={}

#4 : Resumes token dictionary and experience filter
for fn in os.listdir('.'):
     if os.path.isfile(fn) and fn.endswith(".txt"):
        #print (fn)
        total_profiles+=1
        with io.open(fn, "r", encoding="utf-8", errors='ignore') as my_file:
         filecontent = my_file.read() #filecontent=open(fn).read()
        before, term, after = filecontent.partition('years')
        expstr=before.replace("+", " ")
        exp=[int(s) for s in expstr.split() if s.isdigit()]
        yop[fn]=exp[-1]
        #print exp[-1]
        if exp[-1]>=exp_yop:
           tokens = nltk.word_tokenize(filecontent)
           stopword = set(stopwords.words('english'))
           keywords = list(set(tokens).difference(stopword))
           kw_tag=pos_tag(keywords)
           kw_list=[word for word,pos in kw_tag if pos=='NNP']
           keywords_dict[fn]=kw_list
shortlisted_profiles=[]
#set(keywords_dict['17318_Siddesh.txt']) & set(pref_skillset)

#5 : Match-Score of JD-Resume
for key in keywords_dict:
    score_dict[key]={}
    score_dict[key]['years_of_exp']=yop[key]
    score_dict[key]['mandatory_skills_%']=len(set(keywords_dict[key]) & set(mand_skillset))*100/len(mand_skillset)
    if len(set(pref_skillset))>=1:
     score_dict[key]['preferred_skills_%']=len(set(keywords_dict[key]) & set(pref_skillset))*100/len(pref_skillset)
shortlisted_profiles={k:v for k,v in score_dict.items() if score_dict[k]['mandatory_skills_%']>20  and k not in ('JD1.txt','JD2.txt','JD3.txt')}
print 'Total profiles processed : {}'.format(total_profiles)
print 'Shortlisted profiles  : {} '.format(len(shortlisted_profiles))
sorted(shortlisted_profiles.items(), key=lambda x: x[1]['mandatory_skills_%'],reverse=True)

#6 : Convert the dictionary to dataframe and write to a csv file
df = pd.DataFrame(shortlisted_profiles)
dft=df.T
op_file_name='profiles_list_'+jd_file[0:3]+'.csv'
print 'The shortlisted profiles list and corresponding metrics are present in the file '+op_file_name
dft.to_csv(op_file_name)

        
       
