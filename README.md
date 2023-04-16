# MIT 6.0001 Solutions

My solutions to [MIT 6.0001](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/)'s problem sets in Python 3.9. 

Video lectures for this course can be found on [YouTube](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/).


<details>
<summary> <strong>Disclaimer</strong> </summary>
<br>


These solutions were written and published solely for educational and self-study purposes and are **not** guaranteed to be correct. I highly encourage you to attempt solving these psets on your own before checking these solutions, and even so, take them with a grain of salt!

</details>

<details open>
<summary>A note on broken helper code for pset 5</summary>

<br>

As of April 2023, the helper code provided on OCW's website for problem set 5 breaks when trying to run on Python 3.9. Some modifications had to be made to the original code in order to fix it.

Here are some of the issues I found and fixed:
- A deprecated `base64` decoding method in the `feedparser.py` module had to be removed.
- The `process()` function in `ps5.py` broke when trying to access the `description` property for RSS entries. Accessing the `summary` property instead fixes this. 
- The Yahoo News RSS feed endpoint (http://news.yahoo.com/rss/topstories) had to be removed in order avoid breaking the `process()` function.
- Added more info to the exception handling to the `main_thread` in `ps5.py` using the `traceback` module.

With the changes above, the code now runs fine on Python 3.9 and displays news stories from the Google News RSS feed, using the triggers specified in the `triggers.txt` file to filter stories.

</details>



## About 6.0001
> _[6.0001 Introduction to Computer Science and Programming in Python](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/)_ is intended for students with little or no programming experience. It aims to provide students with an understanding of the role computation can play in solving problems and to help students, regardless of their major, feel justifiably confident of their ability to write small programs that allow them to accomplish useful goals. The class uses the Python 3.5 programming language.