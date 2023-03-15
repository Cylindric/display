First signup and get an API token from  https://test.pypi.org/manage/account/#api-tokens

# Test
```bash
pip install --upgrade pytest 
```
# Build
```bash
sudo apt-get install -y python3.10-venv
pip install --upgrade build
pip install --upgrade twine
python3 -m build
```

# Publish
```bash
python3 -m twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps dashboard
```
