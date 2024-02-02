import sys
import argparse

from langora import Langora
from db.dbvector import STORE

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='Langora',
            description='Langora Command Line Interface')
    subparsers = parser.add_subparsers(help='commands', dest='command')

    # ---------------------------------------------------------------------------
    # Install 
    parser_install = subparsers.add_parser('install', help='Initilize Langora knowledge base')
    parser_install.add_argument('-a', '--agent', help="Agent profile description", required=True)
    parser_install.add_argument('-t', '--topics', help="List of topics", nargs='+', required=True)
    #Option 
    parser_install.add_argument('-l', '--load', help="Import level search[DEFAULT]->source->extract->summary",
                                choices=['search', 'source', 'extract', 'summary'], default='search')    
    
    # ---------------------------------------------------------------------------
    # Update
    parser_fill = subparsers.add_parser('update', help='Update knowledge base')
    parser_fill.add_argument('-l', '--load', help="Import level search[DEFAULT]->source->extract->summary",
                             choices=['search', 'source', 'extract', 'summary'], default='search')    
    parser_fill.add_argument('-t', '--task', help="Use task mode", action="store_true")    

    args = parser.parse_args()

    # ---------------------------------------------------------------------------
    # Install  
    # ---------------------------------------------------------------------------
    if args.command == 'install':         
        if not query_yes_no('Are you sure ? It will erase all the database', default='no'):
            sys.exit()
        up_to_store = STORE.SEARCH
        if args.load.lower() == 'source': up_to_store = STORE.SOURCE
        elif args.load.lower() == 'extract': up_to_store = STORE.SRC_EXTRACT
        elif args.load.lower() == 'summary': up_to_store = STORE.SRC_SUMMARY
        
        app = Langora()        
        app.install_db_knowledge(args.agent, args.topics, 
                                 up_to_store=up_to_store)
        
    # ---------------------------------------------------------------------------
    # Update
    # ---------------------------------------------------------------------------
    elif args.command == 'update':

        up_to_store = STORE.SEARCH
        if args.load.lower() == 'source': up_to_store = STORE.SOURCE
        elif args.load.lower() == 'extract': up_to_store = STORE.SRC_EXTRACT
        elif args.load.lower() == 'summary': up_to_store = STORE.SRC_SUMMARY

        app = Langora(is_task_mode=args.task)
        app.update_db_knowledge(up_to_store=up_to_store)

