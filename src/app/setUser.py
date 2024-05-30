from sqllite3_script import set_user
import argparse

def main():
    parser = argparse.ArgumentParser(description='BUser Anlegen')
    parser.add_argument('--name', type=str, required=True, help='Benutzername')
    parser.add_argument('--password', type=str, required=True, help='Password')
    	

    args = parser.parse_args()
    set_user(args.name, args.password)

    print(f'User angelegt')

if __name__ == '__main__':
    main()