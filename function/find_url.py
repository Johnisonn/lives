

def find_urls(str):
    path = '/home/uos/Desktop/'
    with open(f'{path}live.txt', 'r') as file_in, open(f'{path}rsv.txt', 'a') as file_out:
        for line in file_in:
            if str in line:
                line = line.strip()
                line = line.split('$')[0]
                line = f'{line}$RSV\n'
                file_out.write(line)



if __name__ == '__main__':
    find_urls('113.57.111.4:1111')