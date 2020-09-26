def argSortStrList(str_list):
    sorted_list = sorted(str_list)
    argSort = []
    prev_index=-1
    for i in range(len(sorted_list)):
        if (i>0) and (sorted_list[i-1]==sorted_list[i]):
            argSort.append(str_list.index(sorted_list[i],prev_index+1))
            prev_index = argSort[-1]
        else:
            argSort.append(str_list.index(sorted_list[i]))
            prev_index = argSort[-1]
    return argSort
