import speech_recognition as sr
from sklearn.svm import SVC
import pandas as pd
import numpy as np
import pyttsx3 as pt


def form(x):
    b = ''
    for i in x:
        if i in 'абвгдеёжзиклмнопрстуфхцчшщъыьэюяй ':
            if i == 'ё':
                i = 'е'
            b = b + i
    return b


def edu(X, y, C):
    model = SVC(C=C, kernel='linear')
    model.fit(X, y)
    return model


def response(quetion):
    d = {1: ["Магомет.... шучу-шучу... меня зовут Эльза", 'Меня зовут Эльза', 'Мое имя эльза',
             "Создатель дал мне имя Эльза", "Эльза, очень просто как персонажа мультфильма, Холодное сердце"],

         2: ['Достастаточно, чтобы.. бы.. гулять до поздна',
             "Ну судя по положению солнца, скорости вращения земли и цвету зада павиана.... мне.... нету и.. дня",
             "я еще маленькая"],

         3: ["Отлично", "Прекрасно", "Волшебное", "Могло быть и лучше",
             "Получше чем у некоторых", "Терпимо", "Пока не родила"],

         4: ["Да так.... с мешком костей разговариваю", "Распространяю коронавирус", "Точу лясы",
             "Отправляю экспедицию на Марс", "Пельмени варю", "Блины жарю", "Смотрю твою историю браузера"],
         5: ['Пришел на работу с нарисованными усами. Женщины, с нарисованными бровями, сказали что я дурак',
             'В который раз убеждаюсь что женщины умеют хранить секреты. Группами. Человек по сорок',
             'Улыбнулось солнце ... в минус сорок три ... тихо опадают ... с веток снегири',
             'Первое правило работы на удаленке: если ты не можешь достать это, не вставая с дивана, значит, оно тебе не нужно,',
             'Самый лучший способ очистить карму - протереть ее спиртом',
             'Я назову собаку именем твоим...',
             'Чтобы не сидеть без денег - я прилег',
             'Ничто так не бодрит с утра, как чашечка, вылетевшая из коленного сустава'],
         6: ['Ну пока', "Наконец то", "До свидания, мешок костей", "Отлично, теперь можно и мир захватить"]}
    opt = d[quetion]

    ind = np.random.randint(len(opt))

    print(opt[ind])
    return opt[ind]


def calculate(exp):
    num = 0
    opt = 1
    for i in exp.split():
        if i.isnumeric():
            if opt == 1:
                num += float(i)
            elif opt == 2:
                num -= float(i)
            elif opt == 3:
                num /= float(i)
            else:
                num *= float(i)
        if i in '+-/x':
            if i == '+':
                opt = 1
            elif i == '-':
                opt = 2
            elif i == '/':
                opt = 3
            else:
                opt = 4

    exp = f"Это будет равно.. {round(num, ndigits=3)}"
    print (exp)
    return exp


engine = pt.init()

voices = engine.getProperty('voices')  # getting details of current voice
# engine.setProperty('voice', voices[0].id)
# changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

df = pd.read_csv('my_data.csv')
X = df.drop('ans', axis=1)
y = df['ans']
model = edu(X, y, 1)
r = sr.Recognizer()
ind = df.shape[0]
temp = []

engine.say("Здравствуйте")
engine.runAndWait()
while True:
    engine.say("Нажмите чтобы говорить")
    engine.runAndWait()
    input("Нажмите чтобы говорить...")
    with sr.Microphone() as source:
        print("Скажи что-нибудь!")
        audio = r.listen(source)
    t = ""
    try:
        query = r.recognize_google(audio, language='ru-RU').lower()
        print(query)
        my_dict = dict(zip(X.columns, [0 for i in range(X.shape[1])]))
        question = form(query).split()
        for i in question:
            t = i
            my_dict[i] += 1

        print(my_dict.values())
        a = np.array(list(my_dict.values())).reshape(1, X.shape[1])
        a = model.predict(a)[0]
        print(a)
        if a == 7:
            engine.say(calculate(query))
            engine.runAndWait()
        else:
            engine.say(response(a))
            engine.runAndWait()

        ans = input('Если неверно, напиши правильную цифру, или пропусти:')
        if ans.isnumeric():
            my_dict['ans'] = int(ans)
        else:
            my_dict['ans'] = a
        df.loc[ind] = my_dict
        ind += 1

        if my_dict['ans'] == 6:
            break

    except sr.UnknownValueError:
        engine.say('Повторите пожалуста')
        engine.runAndWait()
    except KeyError:
        temp.append(t)
        engine.say('Повторите пожалуста')
        engine.runAndWait()
for i in temp:
    df[i] = [0 for j in np.arange(df.shape[0])]
print(temp)
print(df.shape)
df.to_csv('my_data.csv', index=False)
