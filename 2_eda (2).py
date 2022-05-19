#!/usr/bin/env python
# coding: utf-8

# ## Homework #5. Exploratory Data Analysis
# 
# #### Author: `Ivan Moshchenko`
# 
# #### Total time spent on h/w (in minutes): ~2500
# 

# In[20]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

DIALOGS_MERGED_DATA_PATH = "C:/musor/data/merged_data/dialogs_data_all.csv"
DIALOGS_META_MERGED_DATA_PATH = "C:/musor/data/merged_data/dialogs_users_all.csv"

df = pd.read_csv(DIALOGS_MERGED_DATA_PATH)
df_meta = pd.read_csv(DIALOGS_META_MERGED_DATA_PATH)
my_id = 16594645

user_chats = {}
for i in df_meta['dialog_id']:
    users = []
    for j in df_meta[df_meta['dialog_id']==i]['users']:
        users.append(j)
    user_chats[i] = users
df_merged = df_meta.copy()
users = []
for i in df_merged['dialog_id']:
    users.append(user_chats[i])

df_merged['users'] = users
df_merged = df_merged.drop_duplicates(subset = 'dialog_id', keep = 'first')
df_merged = pd.merge(df, df_merged, on = "dialog_id")
df_merged.rename(columns = {'type_x':'type_message', 'type_y':'type_dialog'}, inplace = True)


# 1)Топ 10 чатів за кількістю тегів мене в них

# In[38]:


m = df_merged[~df_merged['message'].isna()]
m['myTag'] = m['message'].str.contains('@Niva228', na = False, case = False, regex = True)
stat = m[m['myTag']].groupby('name', as_index = False).count()[['name', 'myTag']].sort_values(by='myTag', ascending=False).iloc[:10]
stat['name'] = stat['name'].astype('str')
sns.barplot(x=stat['name'], y=stat['myTag'],)
plt.xticks(rotation=90)
plt.show()


# 2) Топ 15 груп за кількістю стікерів у них

# In[40]:


sticker = df_merged[df_merged['type_message']=='sticker']
tab = sticker.groupby('name', as_index = False)['type_message']
tab = tab.count().sort_values(by='type_message', ascending=False).iloc[:20]
plt.figure(figsize = (8,5))
tab['name'] = tab['name'].astype('str')
sns.barplot(x=tab["name"], y=tab['type_message'],)
plt.ylabel('stickers')
plt.xticks(rotation=90)
plt.show()


# In[28]:


pip install wordcloud


# 3)Хмара повідомлень, які я надсилав брату у вигляді геймпада

# In[71]:


from PIL import *
Image ,
from wordcloud import WordCloud 


file = open(r"C:\musor\russian-stopwords.txt", "r")
ru_stopwords = file.read().splitlines()
file.close()


def create_words(words):
    gamepad = np.array(Image.open('C:\musor\gamepad.png'))
    counterW = pd.value_counts(np.array(words))
    wordsInGamepad = WordCloud(colormap='gist_heat',collocations = False, background_color="white", width=5000, height=3500, 
                      max_words=150,min_font_size = 1,max_font_size = 500,mask = gamepad).generate_from_frequencies(counterW) 
    return wordsInGamepad

def get_words(df):
    vocabulary = []
    for i in df.index:
        for j in str(df['message'][i]).split():
            j.replace(".","")
            j.replace(",","")
            j.replace("?","")
            j.replace("!","")
            if (j != 'nan') and (j not in ru_stopwords) and (j.isalpha()) and (len(j)>3):
                vocabulary.append(j)
    return vocabulary

sent_df = df.loc[df['from_id'] == 'PeerUser(user_id=180562741)']
sent = get_words(sent_df)

gamepad_sent = create_words(sent)
gamepad_figure = plt.figure(figsize=[50,50])
axs = gamepad_figure.add_subplot(1,2,1)
axs.axis('off')
plt.title('', fontsize = 1)
axs.imshow(gamepad_sent)


# 4)Хмара повідомлень, які мені відправляв Брат у вигляді Шреку

# In[72]:


from PIL import *
Image ,
from wordcloud import WordCloud 

file = open(r"C:\musor\russian-stopwords.txt", "r")
ru_stopwords = file.read().splitlines()
file.close()


def create_words(words):
    shrek = np.array(Image.open('C:\musor\shrek.png'))
    counterW = pd.value_counts(np.array(words))
    wordsInShrek = WordCloud(colormap='Pastel1',collocations = False, background_color="black", width=5000, height=3500, 
                      max_words=150,min_font_size = 1,max_font_size = 500,mask = shrek).generate_from_frequencies(counterW) 
    return wordsInShrek

def get_words(df):
    vocabulary = []
    for i in df.index:
        for j in str(df['message'][i]).split():
            j.replace(".","")
            j.replace(",","")
            j.replace("?","")
            j.replace("!","")
            if (j != 'nan') and (j not in ru_stopwords) and (j.isalpha()) and (len(j)>3):
                vocabulary.append(j)
    return vocabulary

received_df = df.loc[df['to_id'] == '180562741']
received = get_words(received_df)

shrek_received = create_words(received)
shrek_figure = plt.figure(figsize=[50,50])
axs = shrek_figure.add_subplot(1,2,1)
axs.axis('off')
plt.title('', fontsize = 1)
axs.imshow(shrek_received)


# 5)Топ 20 груп за кількістю повідомлень

# In[42]:


m = df_merged[df_merged['type_message']=='text']
stat = m.groupby('name', as_index = False)['type_message']
stat = stat.count().sort_values(by='type_message', ascending=False).iloc[:20]
plt.figure(figsize = (8,5))
stat['name'] = stat['name'].astype('str')
sns.barplot(x=stat["name"], y=stat['type_message'],)
plt.ylabel('messages')
plt.xticks(rotation=90)
plt.show()


# 6)Топ 5 чатів за кількістю використання абревіатури "кс" в них

# In[43]:


m = df_merged[~df_merged['message'].isna()]
m['cs'] = m['message'].str.contains('кс', na = False, case = False, regex = True)
tab = m[m['cs']].groupby('name', as_index = False).count()[['name', 'cs']].sort_values(by='cs', ascending=False).iloc[:5]
tab['name'] = tab['name'].astype('str')
plt.figure(figsize = (8,5))
sns.barplot(x=tab["name"], y=tab['cs'],)
plt.ylabel('К С')
plt.xticks(rotation=90)
plt.show()


# 7)Топ 7 чатів за кількістю фотографій у них

# In[75]:


photos = df[df['type']=='photo']
tab = photos.groupby('dialog_id', as_index = False)['type']
tab = tab.count().sort_values(by='type', ascending=False).iloc[:7]
tab['dialog_id'] = tab['dialog_id'].astype('str')
plt.figure(figsize = (8,5))
sns.barplot(x=tab["dialog_id"], y=tab['type'],)
plt.ylabel('Photos')
plt.xticks(rotation=90)
plt.show()


# 8)Топ 8 груп за кількістю людей

# In[76]:


groups = df_meta[df_meta['type'] == 'Group']
g_stat = groups.groupby('dialog_id', as_index=False)['users'].count()
g_stat = g_stat.merge(groups[['dialog_id']], on='dialog_id', how='inner').groupby('dialog_id', as_index=False).last().sort_values(by='users', ascending=False).iloc[:8]
g_stat['dialog_id'] = g_stat['dialog_id'].astype('str')
plt.figure(figsize = (8,5))
sns.barplot(x=g_stat["dialog_id"], y=g_stat['users'],)
plt.ylabel('Users')
plt.xticks(rotation=90)
plt.show()


# 9)Скільки разів друг писав меня "кс"

# In[77]:


dialog = df[(df["dialog_id"]==336030816)&(df["type"]=="text")&(df['from_id'].isnull())]["message"]
cs_counter = dialog.str.count("кс").sum()
cs_counter


# 10)Скільки всього повідомлень у нашому із сестрою чаті

# In[79]:


s =len(df.loc[df['from_id'] == 'PeerUser(user_id=62835542)'])
r =len(df.loc[df['to_id'] == "62835542"])
print(s + r)


# 11)У який період часу я переписуюсь більше?
# 

# In[80]:


df_date1 = pd.read_csv(DIALOGS_MERGED_DATA_PATH)
df_date1['date'] = pd.to_datetime(df_date1['date'])
hours = [str(i) for i in range(1,25)]

df1 = df_date1[(df_date1['from_id'] == my_id)]
df1['date'] = df_date1['date'].apply(lambda x: x.hour)

vals = df1.groupby('date')['date'].count()

fig, (ax1) = plt.subplots()
fig.set_size_inches(15,10) 

ax1.bar(hours, vals)
ax1.set_ylabel('Кількість повідомлень')
ax1.set_xlabel('Години')
plt.rcParams['font.size'] = '16'


plt.show()


# 12)Як часто використовується "ок" і "так" у відсотковому співвідношенні

# In[81]:


yes_regexes = ['так|да', "ок|кк"]
yes_expression = ['Так/Да', 'Ок/Кк']
yes_df = pd.DataFrame({'title':yes_expression, 'count':[0, 0]})
for i in range(len(yes_regexes)):
    yes_df.loc[i, 'count'] = df[df['message'].str.contains(yes_regexes[i], case = False, na = False)].shape[0]
plt.pie(yes_df['count'], labels=yes_df['title'], autopct = '%0.0f%%')
plt.show()


# 13)Про яку гру я частіше переписуюсь у відсотковому співвідношенні

# In[82]:


cs_regex = ['кс|cs', "дота|dota"]
cs_expres = ['кс/сs', 'дота/dota']
cs_df = pd.DataFrame({'title':cs_expres, 'count':[0, 0]})
for i in range(len(cs_regex)):
    cs_df.loc[i, 'count'] = df[df['message'].str.contains(cs_regex[i], case = False, na = False)].shape[0]
plt.pie(cs_df['count'], labels=cs_df['title'], autopct = '%0.0f%%')
plt.show()


# In[ ]:




