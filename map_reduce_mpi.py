# Jaime Martinez
# Template provided by David Pruitt

import time
from mpi4py import MPI
import re


def word_count(sentences, word_list):
    # get the world communicator
    comm = MPI.COMM_WORLD

    # get our rank (process #)
    rank = comm.Get_rank()

    # get the size of the communicator in # processes
    size = comm.Get_size()

    # creating unique dicts for each process
    dict_words = {}

    for word, count in dict_words.items():
        dict_words[word] = count * rank

    # the local list for the processes
    local_list = []

    # distributive work
    if rank == 0:

        first_part = sentences[:8//size]
        # distributing the data
        for process in range(1, size):
            # start and end of slice we're sending
            startOfSlice = int(8/size * process)
            endOfSlice = int(8/size * (process + 1))

            print("Start Index", startOfSlice)
            print("END INDEX", endOfSlice)
            if process == 1:
                slice_to_send = sentences[startOfSlice:endOfSlice]
                slice_to_send += first_part

            else:
                slice_to_send = sentences[startOfSlice:endOfSlice]
            comm.send(slice_to_send, dest=process, tag=0)
    else:
        # receive messages
        local_list = comm.recv(source=0, tag=0)

    temp_dict_words = {}

    # iterating through the list of lines
    for line in local_list:
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

    # mpirun -n 4 python3 map_reduce_mpi.py
    if rank == 0:

        # dictionaries receive
        # gather all dictionaries and adding them
        for process in range(1, size):
            received_dict = comm.recv(source=process, tag=0)
            for key, value in received_dict.items():
                if key not in dict_words:
                    dict_words[key] = value
                else:
                    dict_words[key] += value

    else:
        # send the temp dictionaries
        comm.send(temp_dict_words, dest=0, tag=0)

    return dict_words


def main():
    sentences = []

    # reading all files
    for i in range(1, 9):
        text = ""
        with open("/Users/jaimemartinez/PycharmProjects/CS4175/files/shakespeare" + str(i) + ".txt", "r") as file:
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

    rank = MPI.COMM_WORLD.Get_rank()

    if rank == 0:
        print("Elapsed time: " + "{:0.3f}".format(stop) + " seconds")

        print("\nThe number of each instances of each word for the set of documents are:")

        for key, value in dict_words.items():
            print(key,":", value)
        print("\nThe total count of all words in the list is : " + str(sum(dict_words.values())))


if __name__ == '__main__':
    # execute only if run as a script
    main()
