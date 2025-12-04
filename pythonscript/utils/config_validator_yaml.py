import yaml, sys


file = sys.argv[1]
with open(file) as f:
    try:
        data = yaml.safe_load(f)
        print("Config OK")
    except Exception as e:
        print("Error:", e)