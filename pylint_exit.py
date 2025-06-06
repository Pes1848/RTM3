pylint model.py || pylint-exit %ERRORLEVEL%
if [ %ERRORLEVEL% -ne 0 ]; then
  echo "An error occurred while running pylint." >&2
  exit 1
fi
