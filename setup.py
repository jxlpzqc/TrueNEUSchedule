import main

if __name__ == '__main__':
	main.db.drop_all()
	main.db.create_all()
