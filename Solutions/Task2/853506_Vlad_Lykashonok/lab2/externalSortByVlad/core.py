import random

# with open('numbers.txt', 'w') as f:
#     f.writelines('{}\n'.format(random.randint(-1000000, 1000000)) for _ in range(500000000))

import tempfile

def quick_sort(list_to_sort, compare_function = lambda a , b : a > b, reversed = False):
    ''' Sorts list by using (slow) Vlads quicksort from first lab'''
    if len(list_to_sort) == 1:
        return list_to_sort   # if single element, return it
    i = 0                     # left border
    j = len(list_to_sort) - 1 # right border
    pivot = list_to_sort[int((i + j)/2)] 
    while i <= j: # this loop place elements to left if they're less than pivot (and to other side)
        if reversed:
            while compare_function(list_to_sort[i], pivot):
                i+=1
            while compare_function(pivot, list_to_sort[j]):
                j-=1
        else:
            while compare_function(pivot, list_to_sort[i]):
                i+=1
            while compare_function(list_to_sort[j], pivot):
                j-=1
        if i <= j:
            tmp = list_to_sort[j]
            list_to_sort[j] = list_to_sort[i]
            list_to_sort[i] = tmp
            j-=1
            i+=1
    if list_to_sort[i:len(list_to_sort)]: # if not empty, make same action with right part of list
        list_to_sort[i:len(list_to_sort)] = quick_sort(list_to_sort[i:len(list_to_sort)], compare_function, reversed) # right side
    if list_to_sort[0:j + 1]:
        list_to_sort[0:j + 1] = quick_sort(list_to_sort[0:j + 1], compare_function, reversed) # left side
    return list_to_sort # return fully sorted part (one element)

def external_sort(FILE_TO_SORT = "numbers.txt", FILE_TO_OUTPUT = "output.txt",BUFFER_SIZE = 20971520 * 2): #40mb = 20971520 * 2
    '''Sorts file from FILE_TO_SORT and copy sorted values to FILE_TO_OUTPUT. BUFFER_SIZE is 40 mb by default'''
    tmp_files = []
    tmp_files_copy = []
    sort_buffer = [] # for single file

    # with tempfile.TemporaryDirectory(prefix="python_lab_temp_") as temp_directory:
    # cant coverage TemporaryDirectory, cause it uses python2
    with open(FILE_TO_OUTPUT, 'w') as file_to_output:
        with open(FILE_TO_SORT) as file_to_sort:
            #reading buffer of numbers, sorting and throwing them to tmp files
            buffer = ' '
            tmpFileIndex = 0
            buffer = file_to_sort.read(BUFFER_SIZE)
            if not buffer: raise ValueError('empty file, nothing to sort')
            while buffer:
                while buffer[-1] != '\n':
                    buffer += file_to_sort.read(1)
                tmp = tempfile.NamedTemporaryFile(mode="w+", prefix="python_lab_temp_", suffix=".txt")
                tmp_files.append(tmp)
                tmp_files_copy.append(tmp)
                tmp.writelines('{}\n'.format(number) for number in quick_sort(buffer[:len(buffer) - 1].split('\n'), lambda a, b : int(a) > int(b)))
                tmp.seek(0)
                buffer = file_to_sort.read(BUFFER_SIZE)
            
            # merging every pair of files in new file
            file_index = 0
            sorted_file_numbers = []
            while len(tmp_files) != 1:
                merged_file = tempfile.NamedTemporaryFile(mode="w+", prefix="python_lab_temp_", suffix=".txt")
                
                if file_index == len(tmp_files) - 1: file_index = 0
                first_number = (tmp_files[file_index].readline())
                second_number = (tmp_files[file_index + 1].readline())
                while first_number or second_number:
                    if first_number == '':
                        merged_file.write('{}'.format(second_number))
                        second_number = tmp_files[file_index + 1].readline()
                    elif second_number == '':
                        merged_file.write('{}'.format(first_number))
                        first_number = tmp_files[file_index].readline()
                    elif int(first_number) > int(second_number):
                        merged_file.write('{}'.format(second_number))
                        second_number = tmp_files[file_index + 1].readline()
                    else:
                        merged_file.write('{}'.format(first_number))
                        first_number = tmp_files[file_index].readline()

                merged_file.seek(0)
                tmp_files.remove(tmp_files[file_index+1])
                tmp_files[file_index] = merged_file

                if file_index == len(tmp_files) - 1: 
                    file_index = 0
                else: 
                    file_index += 1
            tmp_files[0].seek(0)

            line = tmp_files[0].readline()
            while line:
                file_to_output.write(line)
                line = tmp_files[0].readline()
            tmp_files[0].close()
            tmp_files.remove(tmp_files[0])