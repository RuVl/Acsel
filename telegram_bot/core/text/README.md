## How to compile messages

---

Firstly, create `.pot` file with all by command:
```shell
pybabel extract --sort-by-file --input-dirs=. --ignore-dirs=venv -o core/text/locales/messages.pot
```

---

Generate `.po` file for necessary language by command:
```shell
pybabel init -i core/text/locales/messages.pot -d locales -D messages -l en
```

Or update existing `.po` file by command:
```shell
pybabel update -d core/text/locales -D messages -i core/text/locales/messages.pot
```

---

Compile all messages in `.po` file to `.mo` file by command:
```shell
pybabel compile -d core/text/locales -D messages
```

---