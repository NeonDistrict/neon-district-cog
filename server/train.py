# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from NDChatterBot import NDChatterBot

bot = NDChatterBot.NDChatterBot()

bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("chatterbot.corpus.english")

bot.set_trainer(ListTrainer)
bot.train([
    "How are you?",
    "I am good.",
    "That is good to hear.",
    "Thank you",
    "You are welcome.",
])

bot.train([
    "Is it solveable?",
    "I'm unsure of what you're referring to."
])

bot.train([
    "How do I solve the function core?",
    "I can not tell you. Good luck.",
    "Is it solveable?",
    "It is indeed."
])

bot.train([
    "Solve the function core",
    "[SOLVING...] Resolved.",
    "What is the answer?",
    "Memory bank wiped. Rebooting... Done."
])

