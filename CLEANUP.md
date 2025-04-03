# Cleanup Instructions

The following cleanup tasks should be performed to ensure the code base is clean and consistent:

## Files to Remove

- `app.py`: This file is deprecated and replaced by `elementum_dsa/cli.py`. It contains duplicate functionality that can lead to confusion.

## Manual Steps

1. Remove the deprecated app.py file:
   ```
   git rm app.py
   git commit -m "Remove duplicate app.py file"
   git push
   ```

2. Ensure your Python path is correctly set up if you're running the code directly:
   ```
   export PYTHONPATH=$PYTHONPATH:/path/to/elementum-dsa-project
   ```

## After Installation

After installing the package, verify that:

1. The CLI command works properly:
   ```
   elementum-dsa --help
   ```

2. Sample queries work as expected:
   ```
   elementum-dsa --query "Generate presentation structure" --domain "presentation_development"
   ```
