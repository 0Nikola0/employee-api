# 1. Setup venv
- Create the venv
```bash
python -m venv .venv
```
- Activate the venv
```bash
# for linux
source ./venv/bin/activate

# for windows
./venv/Scripts/activate
```
- Install dependencies
```bash
python -m pip install -r requirements.txt
```

# 2. Fetch employees
<!-- TODO update cmd-->
```bash
python src/scripts/import_employees.py
```

# 3. Start the server
```bash
python src
```

# 4. Access the swagger-ui
<!-- TODO update url -->
On browser go to: http://localhost:8000/docs