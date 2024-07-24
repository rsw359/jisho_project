import gzip

def extract_gz(input_file, output_file):
    # Open the gzip file in text mode
    with gzip.open(input_file, 'rt', encoding='utf-8') as f_in:
        # Open the output file in write mode with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(f_in.read())

if __name__ == "__main__":
   input_file = '/Users/roger/Downloads/JMdict_e_examp.gz'
   output_file = '/Users/roger/allpie/myjisho/jisho/JMdict.txt'
   extract_gz(input_file, output_file)
   print(f" Done, Extracted to {output_file}")
