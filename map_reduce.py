# Jaime Martinez
# Template provided by David Pruitt

import time
import pymp
import re


def word_count(sentences, word_list):
    # creating a shared dict
    dict_words = pymp.shared.dict()

    with pymp.Parallel(1) as p:

        for i in word_list:
            dict_words[i] = 0

        temp_dict_words = {}

        # getting a lock for this parallel region
        search_lock = p.lock

        # iterating through the list of lines
        for line in p.iterate(sentences):
            for i in word_list:
                temp_dict_words[i] = 0

            # Removing the leading spaces and newline characters, as well as
            # other special characters to leave letters and numbers
            # and making it lowercase for more accurate results

            line = line.strip().lower()
            line = re.sub(r"[^a-zA-Z0-9]+", ' ', line)

            # splitting the line into words
            line = line.split()

            # search for word
            for item in line:
                for word in word_list:
                    if word == item:
                        temp_dict_words[word] += 1
            for word in word_list:
                # lock any other thread from accessing shared dictionary
                search_lock.acquire()
                dict_words[word] += temp_dict_words[word]
                # release lock when done
                search_lock.release()
        p.print("Thread number " + str(p.thread_num) + " of " + str(p.num_threads))

    return dict_words


def main():
    sentences = []

    # reading all files
    for i in range(1, 9):
        text = ""
        with open("shakespeare" + str(i) + ".txt", "r") as file:
            for line in file:
                text = text + line
        sentences.append(text)

    words = ["hate", "love", "death", "night", "sleep", "time",
             "henry", "hamlet", "you", "my", "blood", "poison",
             "macbeth", "king", "heart", "honest"]

    # calculating the time it took
    start = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)
    dict_words = word_count(sentences, words)
    stop = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID) - start

    print("Elapsed time: " + "{:0.3f}".format(stop) + " seconds")

    print("\nThe number of each instances of each word for the set of documents are:")
    for key, value in dict_words.items():
        print(key, value)
    print("\nThe total count of all words in the list is : " + str(sum(dict_words.values())))


if __name__ == '__main__':
    # execute only if run as a script
    main()
