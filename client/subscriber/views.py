from django.shortcuts import render
from .thutech_subscriber import Subscriber


def test():
    subscriber = Subscriber('tcp://validator:4004')
    subscriber.start()

