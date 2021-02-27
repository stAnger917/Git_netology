def txt_doc_resulter(a, b):
    with open(a) as txt_file:
        tmp_lst = txt_file.readlines()
        str_len_a = len(tmp_lst)
        t = txt_file.read()

    with open(b) as another_txt_file:
        another_tmp_lst = another_txt_file.readlines()
        str_len_b = len(another_tmp_lst)
        lt = another_txt_file.read()

    if str_len_a < str_len_b:
        with open('result.txt', 'a') as res:
            res.write(f'{a}\n{str_len_a}')
            for line in open(a):
                res.write(line)
            res.write(f'\n{b}\n{str_len_b}\n{lt}')
            for line in open(b):
                res.write(line)
    else:
        with open('result.txt', 'a') as res:
            res.write(f'{b}\n{str_len_b}\n{lt}')
            for line in open(b):
                res.write(line)
            res.write(f'\n{a}\n{str_len_a}\n{t}')
            for line in open(a):
                res.write(line)


txt_doc_resulter('1.txt', '2.txt')

