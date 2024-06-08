import os, re
from VerseTextCollector import verse_extraction

verse_locator = re.compile(r'VERSE: (.+)')
reference_locator = re.compile(r'REFERENCE: (.+)')
verse_range = re.compile(r':(\d+-\d+)')
# hymn_folder_path = '/Users/ryan/Desktop/Projects/Coding Projects/Scriptures Scraping/Hymns'
hymn_folder_path = f'{os.getcwd()}/Hymns'
# conference_folder_path = '/Users/ryan/Desktop/Projects/Coding Projects/Scriptures Scraping/GeneralConference'
conference_folder_path = f'{os.getcwd()}/GeneralConference'



class Hymn:
    def __init__(self, number):
        self.number = number
        self.title = None
        self.url = None
        self.references = []
        self.data_builder()

    def data_builder(self):
        with open(f'{hymn_folder_path}/{self.number}.txt', 'r') as file:
            for line in file:
                if line.startswith('TITLE: '):
                    line = line.replace('TITLE: ', '')
                    line = line.replace('\n','')
                    self.title = line
                elif line.startswith('NUMBER: '):
                    pass
                elif line.startswith('REFERENCE: '):
                    line = line.replace('REFERENCE: ', '')
                    line = line.replace('\n', '')
                    self.references.append(line)
                elif line.startswith('URL: '):
                    line = line.replace('URL: ', '')
                    self.url = line

class Talk:
    def __init__(self, title, conference):
        self.title = title
        self.speaker = None
        self.conference = conference
        self.references = []
        self.url = None

class Verse:

    def __init__(self, name):
        self.name = name
        self.text = None
        self.reference_by = []
        self.reference_to = []
        self.hymn_references = []
        self.talk_references = []

    def add_reference_by(self, reference):
        if isinstance(reference, str) and reference not in self.reference_by:
            self.reference_by.append(reference)
        if isinstance(reference, list):
            for item in reference:
                if item not in self.reference_by:
                    self.reference_by.append(item)

    def add_reference_to(self, reference):
        if isinstance(reference, str) and reference not in self.reference_to:
            self.reference_to.append(reference)
        if isinstance(reference, list):
            for item in reference:
                if item not in self.reference_to:
                    self.reference_to.append(item)


def dictionary_cleanup(dictionary):
    keys_to_remove = []
    for key in dictionary:
        if dictionary[key] == []:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del dictionary[key]
    return dictionary


def dictionary_maker(main_path):
    ref_dic = {}
    sub_folders = [x[0] for x in os.walk(main_path)]
    for folder in sub_folders[1:]:
        for file in os.listdir(folder):
            file_path = os.path.join(main_path, folder, file)
            with open(file_path, "r", encoding='ISO-8859-1') as opened_file:
                for line in opened_file:
                    if bool(verse_locator.search(line)): #Looks for main verse values
                        verse = re.findall(verse_locator, line)[0]
                        reference_list = []
                        ref_dic[verse] = reference_list
                    if bool(reference_locator.search(line)): #Looks for reference values
                        reference = re.findall(reference_locator, line)[0]
                        if bool(verse_range.search(reference)) and ',' not in reference: #splits verse ranges into individual vereses
                            split_reference = reference.split(':') #split reference 0 is the book and chapter and 1 is the verse range
                            verse_split_range = split_reference[1].split('-') #reference 0 is the low verse range, reference 1 is the high range
                            for verse_number in range(int(verse_split_range[0]), int(verse_split_range[1]) + 1):
                                reference_list.append(split_reference[0] + ':' + str(verse_number))
                        elif ',' in reference:
                            split_reference = reference.split(':')
                            chapter_info = split_reference[0]
                            first_reference = split_reference[1].split(',')[0]
                            second_reference = split_reference[1].split(',')[1]
                            if '-' in first_reference:
                                verse_split_range = first_reference.split('-')  # reference 0 is the low verse range, reference 1 is the high range
                                for verse_number in range(int(verse_split_range[0]), int(verse_split_range[1]) + 1):
                                    reference_list.append(chapter_info + ':' + str(verse_number))
                            else:
                                reference_list.append(chapter_info + ":" + first_reference)
                            if '-' in second_reference:
                                verse_split_range = second_reference.split('-')  # reference 0 is the low verse range, reference 1 is the high range
                                for verse_number in range(int(verse_split_range[0]), int(verse_split_range[1]) + 1):
                                    reference_list.append(chapter_info + ':' + str(verse_number))
                            else:
                                reference_list.append(chapter_info + ':' + second_reference)
                        else:
                            reference_list.append(reference)
    with open(main_path + "/dictionary.txt", 'w') as opened_file:
        opened_file.write(str(dictionary_cleanup(ref_dic)))
    return dictionary_cleanup(ref_dic)

def verse_object_constructor(file):
    object_dict = {}
    with open(file, "r") as opened_file:
        all_verses = opened_file.read()
        for line in all_verses.split('\n'):
            object_dict[line] = Verse(line)
    return object_dict

def add_references(set_dictionary, read_dictionary, direction):
    if direction == "to":
        for verse in read_dictionary:
            set_dictionary[verse].add_reference_to(read_dictionary[verse])
    elif direction == "by":
        for verse in read_dictionary:
            set_dictionary[verse].add_reference_by(read_dictionary[verse])
    else:
        print("Invalid direction: Direction must be 'to' or 'by'")

def gen_ref_by(dictionary):
    ref_by = {}
    for verse in dictionary:
        for reference in dictionary[verse]:
            if reference not in ref_by:
                ref_by[reference] = [verse]
            else:
                ref_by[reference].append(verse)
    return dictionary_cleanup(ref_by)

def talk_object_builder(directory):
    talk_dict = {}
    for filename in os.listdir(directory):
        conference = filename[:-4]
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            all_talks = file.read()
            all_talks = all_talks.split('\n')
        for line in all_talks:
            if line.startswith('TITLE: '):
                title = line[len('TITLE: '):]
                talk_object = Talk(title, conference)
            elif line.startswith('AUTHOR: '):
                talk_object.speaker = line[len('AUTHOR: '):]
            elif line.startswith('REFERENCE: '):
                talk_object.references.append(line[len('REFERENCE: '):])
            elif line.startswith('URL: '):
                talk_object.url = line[len('URL:'):]
                talk_dict[f'{talk_object.title} - {talk_object.speaker} - {talk_object.conference}'] = talk_object
            else:
                pass
    return talk_dict


def verse_conf_add(verse_object_dict, conf_dict):
    for key in conf_dict:
        references = conf_dict[key].references
        for verse in references:
            if verse == 'js-h 1:76' or verse == 'js-h 1:77' or verse == 'js-h 1:78' or verse == 'js-h 1:79' or verse == 'js-h 1:80' or verse == 'js-h 1:81' or verse == 'js-h 1:82':
                pass
            else:
                verse_object_dict[verse].talk_references.append(key)



def object_creation():
    # main_path = "/Users/ryan/Desktop/Projects/Coding Projects/Scriptures Scraping/references_by_chapter"
    main_path = f"{os.getcwd()}/references_by_chapter"
    verse_dict = verse_object_constructor('all_verse_numbers.txt')
    footnotes_dict = dictionary_maker(main_path)
    add_references(verse_dict, footnotes_dict, 'to')
    # print(f'Reference to: {verse_dict['matt 28:6'].reference_to}')
    refs_by = gen_ref_by(footnotes_dict)
    add_references(verse_dict, refs_by, 'by')
    # print(f'Referenced by: {verse_dict['matt 28:6'].reference_by}')
    hymns_dict = {}
    for i in range(1, 342):
        hymns_dict[i] = Hymn(i)
        for verse in hymns_dict[i].references:
            verse_dict[verse].hymn_references.append(hymns_dict[i].number)
    # print(f'Hymn References: {verse_dict['matt 28:6'].hymn_references}')
    verse_text_dict = verse_extraction()
    for key in verse_text_dict:
        verse_dict[key].text = verse_text_dict[key]
    conference_dict = talk_object_builder(conference_folder_path)
    verse_conf_add(verse_dict, conference_dict)
    return(verse_dict, hymns_dict, conference_dict)

def get_refs(verse, object_dict):
    return object_dict[verse].reference_to, object_dict[verse].reference_by, object_dict[verse].hymn_references


# add a hymn referencer
# add a general conference referencer - They started doing footnotes in April 2003, before that all references are just links in the text
        # or I could just look for all hrefs that link to somewhere in the scriptures. This would probably be the easiest
# Maybe liahona articles
# Look into the dominate library for HTML construction to display my data

if __name__ == '__main__':
    # main_path = "/Users/ryan/Desktop/Projects/Coding Projects/Scriptures Scraping/references_by_chapter"
    # verse_dict = verse_object_constructor('all_verse_numbers.txt')
    # footnotes_dict = dictionary_maker(main_path)
    # add_references(verse_dict, footnotes_dict, 'to')
    # print(f'Reference to: {verse_dict['matt 28:6'].reference_to}')
    # refs_by = gen_ref_by(footnotes_dict)
    # add_references(verse_dict, refs_by, 'by')
    # print(f'Referenced by: {verse_dict['matt 28:6'].reference_by}')
    # hymns_dict = {}
    # for i in range(1,342):
    #     hymns_dict[i] = Hymn(i)
    #     for verse in hymns_dict[i].references:
    #         verse_dict[verse].hymn_references.append(hymns_dict[i].title)
    # print(f'Hymn References: {verse_dict['matt 28:6'].hymn_references}')
    # print(f'Hymn: {hymns_dict[107].title}, References: {hymns_dict[107].references}, URL: {hymns_dict[107].url}')
    # object_dict = object_creation()
    # print(get_refs('1-ne 1:1', object_dict))
    verse_dict, hymns_dict, conference_dict = object_creation()
    print(verse_dict['ether 12:27'].talk_references)