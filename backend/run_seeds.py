import subprocess

def run_seeds():
    try:
        subprocess.run(['python', 'seed_db.py'], check=True)
        subprocess.run(['python', 'seed_blurbs.py'], check=True)
        subprocess.run(['python', 'seed_questions.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__=='__main__':
    run_seeds()