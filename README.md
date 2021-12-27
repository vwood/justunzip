# justunzip
CLI tool to just unzip a truncated or partially corrupt zipfile

```console
user@bar:~$ unzip -l test.zip 
Archive:  test.zip
  End-of-central-directory signature not found.  Either this file is not
  a zipfile, or it constitutes one disk of a multi-part archive.  In the
  latter case the central directory and zipfile comment will be found on
  the last disk(s) of this archive.
unzip:  cannot find zipfile directory in one of test.zip or
        test.zip.zip, and cannot find test.zip.ZIP, period.

user@bar:~$ unzip test.zip 
Archive:  test.zip
  End-of-central-directory signature not found.  Either this file is not
  a zipfile, or it constitutes one disk of a multi-part archive.  In the
  latter case the central directory and zipfile comment will be found on
  the last disk(s) of this archive.
unzip:  cannot find zipfile directory in one of test.zip or
        test.zip.zip, and cannot find test.zip.ZIP, period.
```

```console
user@bar:~$ justunzip -l test.zip 
Archive: test.zip
Length     Name
---------- ----
         0 justunzip/build/
         0 justunzip/dist/
      1062 justunzip/LICENSE
        76 justunzip/README.md
       823 justunzip/setup.py
         0 justunzip/src/
         0 justunzip/build/bdist.linux-x86_64/
         0 justunzip/build/lib/
         0 justunzip/build/lib/justunzip/
         0 justunzip/build/lib/justunzip/__init__.py
      1936 justunzip/build/lib/justunzip/justunzip.py
      2614 justunzip/dist/justunzip-0.0.1-py3.8.egg

user@bar:~$ justunzip test.zip 
Archive: test.zip
creating: justunzip/LICENSE
creating: justunzip/README.md
creating: justunzip/setup.py
creating: justunzip/build/lib/justunzip/justunzip.py
WARNING:root:b'justunzip/dist/justunzip-0.0.1-py3.8.egg' is truncated
ERROR:root:error decompressing b'justunzip/dist/justunzip-0.0.1-py3.8.egg'
creating: justunzip/dist/justunzip-0.0.1-py3.8.egg
```
