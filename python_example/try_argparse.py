import argparse



if __name__ == "__main__":
    #parse argvs
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-r', '--required', required=True,
                        help="required input")
    parser.add_argument('-o', '--optional',
                        help="optional input")
    args = parser.parse_args()
    required = args.required
    optional = args.optional
    print("User input: -r {} -o {}".format(required, optional))