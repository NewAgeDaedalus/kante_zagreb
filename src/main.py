from argparse import ArgumentParser
from export import export


def parse_arguments():
    #Setup parser
    parser = ArgumentParser(prog="kante_zagreb", description="Exports the kante_zagreb database to csv or json")
    parser.add_argument("command")
    parser.add_argument("-f", "--format")
    parser.add_argument("-o", "--output-file")
    #Check the arguments
    args = parser.parse_args()
    if ( args.command != "export" or (args.format == None or args.output_file == None) ):
        print("Invalid arguments")
        exit(1)
    return args

def main():
    #Parse arguments
    args = parse_arguments()
    #Execute
    if ( args.command == "export"):
        export(args.format, args.output_file)
    else:
        print("Unknown command")
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
