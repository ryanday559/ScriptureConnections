#streamlit run ScriptureReferencesDisplay.py
#Ctrl+c to stop


#â text â is a pattern for quotations
#WordâWord is a pattern for Word-Word
#â in the middle of a word is a pattern for '
#Ã± is ñ

import DataAnalyzer as da
import re
import streamlit as st
import pickle
import os

main_dir = os.getcwd()

with open('ScriptureReferences/object_dict.pickle', 'rb') as file:
    object_dict = pickle.load(file)

with open('ScriptureReferences/hymn_dict.pickle', 'rb') as file:
    hymn_dict = pickle.load(file)

with open('ScriptureReferences/conf_dict.pickle', 'rb') as file:
    conf_dict = pickle.load(file)


# object_dict, hymn_dict, conf_dict = da.object_creation()
verse_isolator = re.compile(r'( \d+:\d+)')
chapter_isolator = re.compile(r'(.+) \d+:\d+')
reverse_chapter_matcher = {'1-ne': '1 Nephi', '2-ne': '2 Nephi', '3-ne': '3 Nephi', '4-ne': '4 Nephi', 'alma': 'Alma', "enos": 'Enos', "ether" : "Ether", "hel" : 'Helaman', "jacob" : "Jacob", 'jarom' : 'Jarom', 'morm':'Mormon', 'moro': 'Moroni', 'mosiah':'Mosiah', 'omni':'Omni', 'w-of-m':'Words of Mormon', 'dc':'D&C', '1-cor':'1 Corinthians', '1-jn':'1 John', '1-pet':'1 Peter', '1-thes':'1 Thessalonians', '1-tim':'1 Timothy', '2-cor':'2 Corinthians', '2-jn':'2 John', '2-pet':'2 Peter', '2-thes':'2 Thessalonians', 'Jude':'jude', '2-tim':'2 Timothy', '3-jn':'3 John', 'acts':'Acts', 'col':'Colossians', 'eph':'Ephesians', 'gal':'Galatians', 'heb':'Hebrews', 'james':'James', 'john':'John', 'luke':'Luke', 'mark':'Mark', 'matt':'Matthew', 'philem':'Philemon', 'philip':'Philippians', 'rev':'Revelation', 'rom':'Romans', 'titus':'Titus', '1-chr':'1 Chronicles', '1-kgs':'1 Kings', '1-sam':'1 Samuel', '2-chr':'2 Chronicles', '2-kgs':'2 Kings', '2-sam':'2 Samuel', 'exek':'Ezekial', 'amos':'Amos', 'dan':'Daniel', 'deut':'Deuteronomy', 'eccl':'Ecclesiastes', 'esth':'Esther', 'ex':'Exodus', 'ezek':'Ezekiel', 'ezra':'Ezra', 'gen':'Genesis', 'hab':'Habakkuk', 'hag':'Haggai', 'hosea':'Hosea', 'isa':'Isaiah', 'jer':'Jeremiah', 'job':'Job', 'joel':'Joel', 'jonah':'Jonah', 'josh':'Joshua', 'judg':'Judges', 'lam':'Lamentations', 'lev':'Leviticus', 'mal':'Malachi', 'micah':'Micah', 'nahum':'Nahum', 'neh':'Nehemiah', 'zeph':'Zephaniah', 'num':'Numbers', 'obad':'Obadiah', 'prov':'Proverbs', 'ps':'Psalm', 'ruth':'Ruth', 'song':'Song of Solomon', 'zech':'Zechariah', 'abr':'Abraham', 'js-h':'JSH', 'js-m':'JSM', 'moses':'Moses', 'a-of-f':'Article of Faith'}
chapter_matcher = {'1 Nephi': '1-ne', '2 Nephi': '2-ne', '3 Nephi': '3-ne', '4 Nephi': '4-ne', 'Alma': 'alma', 'Enos': 'enos', 'Ether': 'ether', 'Helaman': 'hel', 'Jacob': 'jacob', 'Jarom': 'jarom', 'Mormon': 'morm', 'Moroni': 'moro', 'Mosiah': 'mosiah', 'Omni': 'omni', 'Words of Mormon': 'w-of-m', 'D&C': 'dc', '1 Corinthians': '1-cor', '1 John': '1-jn', '1 Peter': '1-pet', '1 Thessalonians': '1-thes', '1 Timothy': '1-tim', '2 Corinthians': '2-cor', '2 John': '2-jn', '2 Peter': '2-pet', '2 Thessalonians': '2-thes', 'Jude':'jude', '2 Timothy': '2-tim', '3 John': '3-jn', 'Acts': 'acts', 'Colossians': 'col', 'Ephesians': 'eph', 'Galatians': 'gal', 'Hebrews': 'heb', 'James': 'james', 'John': 'john', 'Luke': 'luke', 'Mark': 'mark', 'Matthew': 'matt', 'Philemon': 'philem', 'Philippians': 'philip', 'Revelation': 'rev', 'Romans': 'rom', 'Titus': 'titus', '1 Chronicles': '1-chr', '1 Kings': '1-kgs', '1 Samuel': '1-sam', '2 Chronicles': '2-chr', '2 Kings': '2-kgs', '2 Samuel': '2-sam', 'Ezekial':'ezek', 'Amos': 'amos', 'Daniel': 'dan', 'Deuteronomy': 'deut', 'Ecclesiastes': 'eccl', 'Esther': 'esth', 'Exodus': 'ex', 'Ezekiel': 'ezek', 'Ezra': 'ezra', 'Genesis': 'gen', 'Habakkuk': 'hab', 'Haggai': 'hag', 'Hosea': 'hosea', 'Isaiah': 'isa', 'Jeremiah': 'jer', 'Job': 'job', 'Joel': 'joel', 'Jonah': 'jonah', 'Joshua': 'josh', 'Judges': 'judg', 'Lamentations': 'lam', 'Leviticus': 'lev', 'Malachi': 'mal', 'Micah': 'micah', 'Zephaniah':'zeph', 'Nahum': 'nahum', 'Nehemiah': 'neh', 'Numbers': 'num', 'Obadiah': 'obad', 'Proverbs': 'prov', 'Psalm': 'ps', 'Ruth': 'ruth', 'Song of Solomon': 'song', 'Zechariah': 'zech', 'Abraham': 'abr', 'JSH': 'js-h', 'JSM': 'js-m', 'Moses': 'moses', 'Article of Faith':'a-of-f'}
st.set_page_config(page_title="Scripture Connections")
st.title('Scripture Connections')
st.logo('ScriptureReferences/open_scriptures.png')
# user_input = st.text_input('Verse:')

def external_reference(ref_list, class_type):
    st.divider()
    if class_type == 'Hymn':
        st.subheader('Hymns:')
        for ref in ref_list:
            st.write(f'[{hymn_dict[ref].number} - {hymn_dict[ref].title}](%s)' % hymn_dict[ref].url)
    elif class_type == 'Talk':
        st.subheader('Talks:')
        # for ref in ref_list:
        #     st.write(f'[{conf_dict[ref].title} - {conf_dict[ref].speaker} - {conf_dict[ref].conference}](%s)' % conf_dict[ref].url)
        st.write(f'Talk Count: {len(ref_list)}')
        col1, col2, col3 = st.columns(3)
        with col1:
            for i in range(len(ref_list) // 3):
                st.write(f'[{conf_dict[ref_list[i]].title} - {conf_dict[ref_list[i]].speaker} - {conf_dict[ref_list[i]].conference}](%s)' %
                         conf_dict[ref_list[i]].url)
        with col2:
            for i in range(len(ref_list) // 3, (len(ref_list) // 3) * 2):
                st.write(f'[{conf_dict[ref_list[i]].title} - {conf_dict[ref_list[i]].speaker} - {conf_dict[ref_list[i]].conference}](%s)' %
                         conf_dict[ref_list[i]].url)
        with col3:
            for i in range((len(ref_list) // 3) * 2, (len(ref_list) // 3) * 3):
                st.write(
                    f'[{conf_dict[ref_list[i]].title} - {conf_dict[ref_list[i]].speaker} - {conf_dict[ref_list[i]].conference}](%s)' %
                    conf_dict[ref_list[i]].url)
        remainder = len(ref_list) % 3
        if remainder == 2:
            i = (len(ref_list) // 3) * 3
            col1.write(f'[{conf_dict[ref_list[i]].title} - {conf_dict[ref_list[i]].speaker} - {conf_dict[ref_list[i]].conference}](%s)' % conf_dict[ref_list[i]].url)
            col2.write(f'[{conf_dict[ref_list[i + 1]].title} - {conf_dict[ref_list[i + 1]].speaker} - {conf_dict[ref_list[i + 1]].conference}](%s)' % conf_dict[ref_list[i + 1]].url)
        elif remainder == 1:
            i = (len(ref_list) // 3) * 3
            col1.write(f'[{conf_dict[ref_list[i]].title} - {conf_dict[ref_list[i]].speaker} - {conf_dict[ref_list[i]].conference}](%s)' % conf_dict[ref_list[i]].url)

def verse_propifier(verse_code):
    chapter = re.findall(chapter_isolator, verse_code)[0]
    if chapter in reverse_chapter_matcher:
        chapter = reverse_chapter_matcher[chapter]
    return chapter + re.findall(verse_isolator, verse_code)[0]


def ref_display(verse_list, direction):
    st.divider()
    if direction == 'To':
        st.subheader(f'References {direction}:')
    elif direction == 'By':
        st.subheader(f'Referenced {direction}:')
    for verse in verse_list:
        proper_verse = verse_propifier(verse)
        with st.expander(proper_verse):
            st.write(object_dict[verse].text)
            reference_button = st.button(f'References for {proper_verse}', key=f'{verse}-{direction}')
            if bool(reference_button):
                return proper_verse

def history_sidebar(hist_list):
    with st.sidebar:
        st.subheader('Reference History:')
        if len(hist_list) == 0:
            return None
        for i in range(len(hist_list)):
            verse_button = st.button(hist_list[i], key=f'{hist_list[i]}-{i}')
            if bool(verse_button):
                return hist_list[i]


def page_constructor():
    if 'verse' in st.session_state.keys():
        user_input = st.text_input('Verse:', value=st.session_state['verse'])
        if user_input == st.session_state['verse']:
            user_input = st.session_state['verse']
    else:
        user_input = st.text_input('Verse:')
    with st.container(border=False):
        if user_input == "":
            st.write("""
            Welcome to Scripture Connections\n
            Please type a valid verse into the search bar\n
            Upon searching a scripture, you will see the verse itself, the references to this scripture which are the references contained within the footnotes, the verses that this scripture is referenced by in the footnotes of verses anywhere else in the standard works, hymns that contain references to that verse (if there are any), and all talks since 1971 that reference this verse or the chapter containing this verse in footnotes or in text references.\n
            Note: All books use their full names except for Doctrine and Covenants, Joseph Smith Matthew, and Jospeh Smith History which are abbreviated as D&C, JSM, and JSH respectively. Please use proper capitalization of book names. For example, use 1 Nephi 1:1 instead of 1 nephi 1:1 or Words of Mormon 1:1 instead of Words of mormon 1:1.
            """)
        try:
            chapter = re.findall(chapter_isolator, user_input)[0][:]
            verse = re.findall(verse_isolator, user_input)[0]
            if chapter not in chapter_matcher:
                raise IndexError
            code_verse = str(chapter_matcher[chapter] + verse)
            if code_verse not in object_dict:
                raise IndexError
            if 'history' not in st.session_state.keys():
                st.session_state['history'] = []
                st.session_state['history'].append(user_input)
            elif user_input != st.session_state['history'][-1]:
                st.session_state['history'].append(user_input)
            history_pressed = history_sidebar(st.session_state['history'])
            if history_pressed is not None:
                st.session_state.verse = history_pressed
                st.rerun()
            if chapter in chapter_matcher:
                st.title(user_input)
                # code_verse = str(chapter_matcher[chapter] + verse)
                st.write(object_dict[code_verse].text)
                verse_clicked = ref_display(object_dict[code_verse].reference_to, 'To')
                if verse_clicked is not None:
                    st.write(verse_clicked)
                    st.session_state.verse = verse_clicked
                    st.rerun()
                verse_clicked = ref_display(object_dict[code_verse].reference_by, 'By')
                external_reference(object_dict[code_verse].hymn_references, 'Hymn')
                external_reference(object_dict[code_verse].talk_references, 'Talk')
                if verse_clicked is not None:
                    st.write(verse_clicked)
                    st.session_state.verse = verse_clicked
                    st.rerun()
        except IndexError or KeyError:
            if user_input == '':
                pass
            else:
                st.write(f':red[Invalid Input:] Please check spelling, capitalization, or that the verse exists.')
                st.write('Search Example: 1 Nephi 3:7')
                if 'history' in st.session_state:
                    history_sidebar(st.session_state['history'])

page_constructor()





