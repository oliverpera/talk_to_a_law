from sqllite3_script import delete_user
import argparse

def main():
    parser = argparse.ArgumentParser(description='User Anlegen')
    parser.add_argument('--name', type=str, required=True, help='Benutzername')

    	
    args = parser.parse_args()
    delete_user(args.name)

    print(f'User gelöscht')

if __name__ == '__main__':
    main()