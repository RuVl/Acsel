## How to compile messages

---

Firstly, create `.pot` file with all by command:

> Specify `-j` parameter if you need to add messages 

```shell
grep -r -l --include=\*.py '^\s*[^#]*_(.*)' ./ |
xargs xgettext --from-code=UTF-8 -L Python -p locales/ -o messages.pot
```

---

Change `.pot` file (set encoding, etc.) \
After that, generate `.po` file for necessary language by command:

```shell
msginit -l ru_RU.UTF-8 --no-translator -i locales/messages.pot -o locales/ru/LC_MESSAGES/messages.po
```

---

Translate all messages in `.po` file and compile file by command:

> If you have an error - try to set charset to UTF-8 in `.po` file

```shell
msgfmt -o locales/ru/LC_MESSAGES/messages.mo locales/ru/LC_MESSAGES/messages.po
```

---