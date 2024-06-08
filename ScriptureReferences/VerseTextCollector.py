import os, re
main_dir = os.getcwd()
chapter_matcher = {'1nephi': '1-ne', '2nephi': '2-ne', '3nephi': '3-ne', '4nephi': '4-ne', 'alma': 'alma', 'Enos': 'enos', 'ether': 'ether', 'helaman': 'hel', 'jacob': 'jacob', 'Jarom': 'jarom', 'mormon': 'morm', 'moroni': 'moro', 'mosiah': 'mosiah', 'Omni': 'omni', 'wordsofmormon': 'w-of-m', 'dc': 'dc', '1corinthians': '1-cor', '1john': '1-jn', '1peter': '1-pet', '1thessalonians': '1-thes', '1timothy': '1-tim', '2corinthians': '2-cor', '2john': '2-jn', '2peter': '2-pet', '2thessalonians': '2-thes', 'jude':'jude', '2timothy': '2-tim', '3john': '3-jn', 'acts': 'acts', 'collosians': 'col', 'ephesians': 'eph', 'galatians': 'gal', 'hebrews': 'heb', 'james': 'james', 'john': 'john', 'luke': 'luke', 'mark': 'mark', 'matthew': 'matt', 'Philemon': 'philem', 'philippians': 'philip', 'revelation': 'rev', 'romans': 'rom', 'titus': 'titus', '1chronicles': '1-chr', '1kings': '1-kgs', '1samuel': '1-sam', '2chronicles': '2-chr', '2kings': '2-kgs', 'ezekial':'ezek', '2samuel': '2-sam', 'amos': 'amos', 'daniel': 'dan', 'deuteronomy': 'deut','zephaniah':'zeph', 'ecclesiastes': 'eccl', 'esther': 'esth', 'exodus': 'ex', 'ezekiel': 'ezek', 'ezra': 'ezra', 'genesis': 'gen', 'habakkuk': 'hab', 'haggai': 'hag', 'hosea': 'hosea', 'isaiah': 'isa', 'jeremiah': 'jer', 'job': 'job', 'joel': 'joel', 'jonah': 'jonah', 'joshua': 'josh', 'judges': 'judg', 'lamentations': 'lam', 'leviticus': 'lev', 'malachi': 'mal', 'micah': 'micah', 'nahum': 'nahum', 'nehemiah': 'neh', 'numbers': 'num', 'Obadiah': 'obad', 'proverbs': 'prov', 'psalm': 'ps', 'ruth': 'ruth', 'song of solomon': 'song', 'zechariah': 'zech', 'abraham': 'abr', 'josephSmithHistory': 'js-h', 'josephSmithMatthew': 'js-m', 'moses': 'moses', 'theArticlesOfFaith':'a-of-f'}
main_folder = f'{main_dir}/markdown-scriptures/'
all_verse_path = f'{main_dir}/all_verse_numbers.txt'
not_open = ['.Ds_store', "01titlepage.md", '02introduction.md', '06briefexplanationaboutthebookofmormon.md', '03testimonyofthreewitnesses.md', '05testimonyoftheprophetjosephsmith.md', '04testimonyofeightwitnesses.md']
folders_to_visit = ['Book of Mormon', 'Doctrine and Covenants', 'New Testament', 'Old Testament', 'Pearl of Great Price']
verse_isolator = re.compile(r'\d+\.(?: )?\n.+')
find_verse_text = re.compile(r'\d+\.(?: )?\n(.+)')
find_verse_number = re.compile(r'(\d+)\.(?: )?\n.+')
find_chapter_number = re.compile(r'(\d+)\.md')

def verse_extraction():
    all_verses = {}
    for work in folders_to_visit:
        folder_path = main_folder + work + '/'
        for folder in os.listdir(folder_path):
            if folder != '.DS_Store' and not folder.startswith('dc'):
                for chapter in os.listdir(folder_path + folder):
                    if chapter not in not_open:
                        with open(f'{folder_path}{folder}/{chapter}', 'r', encoding='ISO-8859-1') as file:
                            chapter_text = file.read()
                        chapter_text = chapter_text.split('## ')[1:]
                        try:
                            chapter_number = re.findall(find_chapter_number, chapter)[0]
                            book = chapter[:-(3 + len(chapter_number))]
                            book = chapter_matcher[book]
                            if chapter_number.startswith('0'):
                                chapter_number = chapter_number[1:]
                        except IndexError:
                            if chapter != '.DS_Store':
                                chapter_number = '1'
                                book = chapter[:-3]
                                book = chapter_matcher[book]
                        for verse in chapter_text:
                            if bool(re.finditer(verse_isolator, verse) and verse != ''):
                                verse_number = re.findall(find_verse_number, verse)[0]
                                verse_text = re.findall(find_verse_text, verse)[0]
                                complete_verse = f'{book} {chapter_number}:{verse_number}'
                                all_verses[complete_verse] = verse_text
            elif folder != '.DS_Store':
                with open(f'{folder_path}{folder}', 'r', encoding='ISO-8859-1') as file:
                    chapter_text = file.read()
                chapter_text = chapter_text.split('## ')[1:]
                chapter_number = re.findall(find_chapter_number, folder)[0]
                if chapter_number.startswith('0'):
                    chapter_number = chapter_number[1:]
                    if chapter_number.startswith('0'):
                        chapter_number = chapter_number[1:]
                book = folder[:-6]
                for verse in chapter_text:
                    if bool(re.finditer(verse_isolator, verse) and verse != ''):
                        verse_number = re.findall(find_verse_number, verse)[0]
                        verse_text = re.findall(find_verse_text, verse)[0]
                        complete_verse = f'{book} {chapter_number}:{verse_number}'
                        all_verses[complete_verse] = verse_text
    return all_verses

if __name__ == '__main__':
    all_verses = verse_extraction()
    print(all_verses['1-thes 1:14'])
