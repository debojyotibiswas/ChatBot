import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import requests
from process import process_ip, process_status1,process_status2,process_status3

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
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

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    #x = 1 / 0
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        
        mal = []
        env = []
        serv = []
        ip = []
        responses = []
        
        if tag == 'status':
            for tg in data['intents']:
                if tg['tag'] == tag:
                    for malcode in tg['parameters']['malcode']:
                        if malcode in inp.lower():
                            mal.append(malcode)

                    for environment in tg['parameters']['env']:
                        if environment in inp.lower():
                            env.append(environment)

                    for server in tg['parameters']['servers']:
                        if server in inp.lower():
                            serv.append(server)

                    ip = process_ip(inp.lower())
                    
                    if len(ip) > 0 and all([len(mal),len(env),len(serv)]) == 0:
                        if len(ip) == 1:
                            process_status3(ip.pop())
                        else:
                            responses = tg['additional-ip']
                    elif (len(mal) == 1 and all([len(env),len(serv)]) == 0) or (len(env) == 1 and all([len(env),len(mal)]) == 0) or all([len(mal),len(env),len(serv)]) == 1 and len(ip) == 0:

                        inp_string = ''
                        if len(mal) != 0: inp_string += mal.pop() + ' '
                        if len(env) != 0: inp_string += env.pop() + ' '
                        if len(serv) != 0: inp_string += serv.pop()
                        if (len(inp_string.split()) < 3): process_status1(inp_string)
                        else: process_status2(inp_string)
                    
                    elif len(mal) > 1 and all([len(env),len(serv)]) <= 1 and len(ip) == 0:
                        responses = tg['additional-malcode']
                    
                    elif len(env) > 1 and all([len(mal),len(serv)]) <= 1 and len(ip) == 0:
                        responses = tg['additional-environment']

                    elif len(serv) > 1 and all([len(env),len(mal)]) <= 1 and len(ip) == 0:    
                        responses = tg['additional-servername']

                    else:
                        responses = tg['responses']

                    if len(responses) != 0:
                        print(random.choice(responses))
                        print(tg['correct-format'])
        else:
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            print(random.choice(responses))


chat()