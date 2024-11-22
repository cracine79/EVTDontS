# import subprocess

# def run_seeds():
#     try:
#         subprocess.run(['python', 'seed_db.py'], check=True)
#         print('Finished One')
#         subprocess.run(['python', 'seed_blurbs.py'], check=True)

#         print('Finished Two')
#         subprocess.run(['python', 'seed_questions.py'], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred: {e}")

# if __name__=='__main__':
#     run_seeds()
from backend.seed_db import main as seed_db_main
from backend.seed_blurbs import main as seed_blurbs_main
from backend.seed_questions import main as seed_questions_main

def run_seeds():
    try:
        print("Running seed_db...")
        seed_db_main()
        print("Finished seeding DB")

        print("Running seed_blurbs...")
        seed_blurbs_main()
        print("Finished seeding blurbs")

        print("Running seed_questions...")
        seed_questions_main()
        print("Finished seeding questions")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    run_seeds()
