import pickle
import json
import random
import tensorflow
import tflearn
import numpy
import re
from nltk.stem.lancaster import LancasterStemmer
import nltk
nltk.download('punkt')
stemmer = LancasterStemmer()


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


with open("utils/intents.json") as file:
    data = json.load(file)

try:
    with open("utils/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("utils/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("utils/model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("utils/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def isPresent(val):
    with open("utils/intents.json") as file:
        data = json.load(file)

    response = []
    d = data['intents']
    myDict = {}
    for j in d:
        myDict[j['tag']] = j['responses']
    for x in d:
        wd = []
        for sentence in x['patterns']:
            w = sentence.split()
            wd = wd+w
        for w in wd:
            if w.lower() == val.lower():
                response.append(x['tag'])
    output = []
    for r in response:
        if r not in output:
            output.append(r)
    if len(output) == 1:
        response = myDict.get(output[0])
        listToStr = ' '.join(map(str, response))
        return listToStr
    elif len(output) > 1:
        return "Please enter the appropriate product name."
    elif findWholeWord("hi")(val) or findWholeWord("hello")(val) or findWholeWord("whats up")(val) or findWholeWord("Is anyone there?")(val) or findWholeWord("good day")(val) or findWholeWord("hey")(val):
        return "Hello friend. Nice to meet you"
    elif findWholeWord('how are')(val) or findWholeWord('how are you?')(val) or findWholeWord('how are you doing?')(val) or findWholeWord('what is your age?')(val):
        return "I sexually identify as a retail store bot here to tell about the location of our products. Please dont ask my age"
    elif findWholeWord("Bye")(val) or findWholeWord("See you later")(val) or findWholeWord("Goodbye")(val):
        return "bye. See you later"
    elif findWholeWord("What hours are you open?")(val) or findWholeWord("What are your hours?")(val) or findWholeWord("When are you open?")(val):
        return "We're open every day 9am-9pm"
    elif findWholeWord("Do you take credit cards?")(val) or findWholeWord("Do you accept Mastercard?")(val) or findWholeWord("Are you cash only?")(val):
        return "We accept VISA, Mastercard and AMEX. We accept most major credit cards"
    elif findWholeWord("Thanks")(val) or findWholeWord("Thank you")(val) or findWholeWord("That's helpful")(val):
        return "Happy to help!"
    elif findWholeWord("help")(val) or findWholeWord("can you help me")(val) or findWholeWord('I need a product')(val):
        return "Please enter a valid product and we can help you out with it"
    else:
        return "I cant get you. Please try a different word."


def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        if results[results_index] > 0.2:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            print(random.choice(responses))
        else:
            print("I didnt get that. Try again")


def results(inp):
    if findWholeWord('how are')(inp) or findWholeWord('how are you?')(inp) or findWholeWord('how are you doing?')(inp) or findWholeWord('what is your age?')(inp) or findWholeWord('Who are you')(inp):
        return "I identify as a retail store bot here to tell about the location of our products. Please dont ask my age"
    else:
        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        if results[results_index] > 0.95:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    return random.choice(responses)
        else:
            op = isPresent(inp)
            print(op)
            return op
