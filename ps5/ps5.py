# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import traceback


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.summary)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================

# Problem 1


class NewsStory:
    '''
    A class for abstractly representing news stories.
    '''

    def __init__(self, guid: str, title: str, description: str, link: str, pubdate: datetime):
        '''
        Initializes a new instance of the NewsStory class.

        guid (string): a globally unique identifier (GUID) 
        title (string): the story's title
        description (string): the story's description
        link (string): a URL to the news story and more content
        pubdate (datetime): the story's publish date

        A NewsStory instance has the following attributes:

            self.guid

            self.title

            self.description

            self.link

            self.pubdate
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        '''
        Used to safely access self.guid outside of the class

        returns: self.guid (string)
        '''
        return self.guid

    def get_title(self):
        '''
        Used to safely access self.title outside of the class

        returns: self.title (string)
        '''
        return self.title

    def get_description(self):
        '''
        Used to safely access self.description outside of the class

        returns: self.description (string)
        '''
        return self.description

    def get_link(self):
        '''
        Used to safely access self.link outside of the class

        returns: self.link (string)
        '''
        return self.link

    def get_pubdate(self):
        '''
        Used to safely access self.pubdate outside of the class

        returns: self.pubdate (datetime)
        '''
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story: NewsStory):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger


def phrase_words_in_text_words(phrase_words: list[str], text_words: list[str]):
    '''
    phrase_words (list[str])
    text_words (list[str])
    '''
    # loop over words in the text
    for i in range(len(text_words)):
        word = text_words[i]
        if (word == phrase_words[0]):

            # found a match
            if (len(phrase_words) == 1):
                # if phrase only has a single word, we're done (base case)
                return True
            # no match: recursive case
            else:
                return phrase_words_in_text_words(phrase_words[1:], text_words[i+1:])

    return False


class PhraseTrigger(Trigger):

    def __init__(self, phrase: str):
        Trigger.__init__(self)
        self.phrase = phrase.lower()

    def is_phrase_in(self, text: str):
        '''
        Returns True if the whole phrase `phrase` is present in text, returns False otherwise.

        `text` (string): the text snippet to test `phrase` against
        '''

        # pre-process text snippet, remove punctuation
        new_text = text.lower()
        for char in string.punctuation:
            if char in new_text:
                new_text = new_text.replace(char, ' ')

        # split into words
        text_words = new_text.split()
        phrase_words = self.phrase.split()

        # check if text contains phrase's first word
        first_match_index = -1

        for i in range(len(text_words)):
            text_word = text_words[i]
            if (text_word == phrase_words[0]):
                # got match of first word
                first_match_index = i
                break

        if (first_match_index == -1):
            # first phrase word couldn't be found
            return False
        else:
            # slice text words starting at first match
            text_words = text_words[i:]

            # phrase has more words than sliced text
            if (len(phrase_words) > len(text_words)):
                return False

            # checking if words match up consecutively
            for i in range(1, len(phrase_words)):
                if (text_words[i] != phrase_words[i]):
                    return False

            # passed all checks!
            return True


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase: str):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story: NewsStory):
        return PhraseTrigger.is_phrase_in(self, story.title)


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase: str):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story: NewsStory):
        return PhraseTrigger.is_phrase_in(self, story.description)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.


class TimeTrigger(Trigger):
    def __init__(self, date_string: str):
        '''
        Creates a new TimeTrigger instance.

        `date_string` (str): a time string in EST in the format of "3 Oct 2016 17:00:10".
        '''
        Trigger.__init__(self)
        self.date = datetime.strptime(
            date_string, '%d %b %Y %H:%M:%S').replace(tzinfo=pytz.timezone('EST'))


# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def __init__(self, date_string: str):
        TimeTrigger.__init__(self, date_string)

    def evaluate(self, story: NewsStory):
        return self.date > story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))


class AfterTrigger(TimeTrigger):
    def __init__(self, date_string: str):
        TimeTrigger.__init__(self, date_string)

    def evaluate(self, story: NewsStory):
        return self.date < story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, t: Trigger):
        Trigger.__init__(self)
        self.t = t

    def evaluate(self, story: NewsStory):
        return not self.t.evaluate(story)


# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, t1: Trigger, t2: Trigger):
        Trigger.__init__(self)
        self.t1 = t1
        self.t2 = t2

    def evaluate(self, story: NewsStory):
        return self.t1.evaluate(story) and self.t2.evaluate(story)


# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, t1: Trigger, t2: Trigger):
        Trigger.__init__(self)
        self.t1 = t1
        self.t2 = t2

    def evaluate(self, story: NewsStory):
        return self.t1.evaluate(story) or self.t2.evaluate(story)

# ======================
# Filtering
# ======================

# Problem 10


def filter_stories(stories: list[NewsStory], triggerlist: list[Trigger]):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtered_stories = []

    for story in stories:
        for trigger in triggerlist:
            if (trigger.evaluate(story)):
                filtered_stories.append(story)

    return filtered_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    triggers = {}
    triggerlist = []

    for line in lines:
        args = line.split(',')
        if (args[0] == 'ADD'):
            for trigger_name in args[1:]:
                triggerlist.append(triggers[trigger_name])
        else:
            trigger_name = args[0]
            trigger_type = args[1]

            # title triggers
            if (trigger_type == 'TITLE'):
                triggers[trigger_name] = TitleTrigger(args[2])

            # description triggers
            if (trigger_type == 'DESCRIPTION'):
                triggers[trigger_name] = DescriptionTrigger(args[2])

            # after triggers
            if (trigger_type == 'AFTER'):
                triggers[trigger_name] = AfterTrigger(args[2])

            # before triggers
            if (trigger_type == 'BEFORE'):
                triggers[trigger_name] = BeforeTrigger(args[2])

            # not trigger
            if (trigger_type == 'NOT'):
                t = triggers[args[2]]
                triggers[trigger_name] = NotTrigger(t)

            # and trigger
            if (trigger_type == 'AND'):
                t1 = triggers[args[2]]
                t2 = triggers[args[3]]
                triggers[trigger_name] = AndTrigger(t1, t2)

            # or trigger
            if (trigger_type == 'OR'):
                t1 = triggers[args[2]]
                t2 = triggers[args[3]]
                triggers[trigger_name] = OrTrigger(t1, t2)

    return triggerlist


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        pubdateShown = []

        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print('ERROR', traceback.format_exc())


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
