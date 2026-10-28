FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/
COPY ./tobybot_engine.py /code/
COPY ./thesaurus.txt /code/
COPY ./word_endings.txt /code/
COPY ./words_to_remove.txt /code/
COPY ./words_to_remove_from_end_of_question.txt /code/
COPY ./words_not_allowed_in_questions.txt /code/
COPY ./index.html /code/
COPY ./about.html /code/
COPY ./toby_bot.jpg /code/static/
COPY ./script.js /code/static/
COPY ./styles.css /code/static/

CMD ["fastapi", "run", "main.py", "--port", "80"]

