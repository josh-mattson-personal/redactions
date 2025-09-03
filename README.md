## About
This code will redact information from an Amazon Data dump

## Instructions
1) Clone this repository
2) Copy your `All Data Categories.zip` file to this directory, and unzip it - directory should be titled `All Data Categories`
3) Fill out any strings you wish to be redacted in `redaction_strings.txt` - every line is a separate entry, any matches will be replaced with `[redacted]`
4) Optional: Use `test_strings.txt` to test the parser, strings found will not be redacted
5) run `python3 main.py`