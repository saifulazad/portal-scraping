import sys
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

from bulk_job_processor import get_all_job_details, read_jobs_links

def main(filename, format):
    links = read_jobs_links(filename)
    get_all_job_details(links)




if __name__ == '__main__':
    # main()
    if len(sys.argv) < 2:
        print('Give file path')
        sys.exit()
    
    main(sys.argv[1], '')
