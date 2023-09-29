# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request
from flask_login import login_required
import os
import sys
import time
import openai

blueprint = Blueprint(
    "user", __name__, url_prefix="/users", static_folder="../static"
)

openai.api_key = "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"

systemPrompt = {"role": "system", "content": "You are a helpful assistant."}
data = []


def get_gpt(incoming_msg):
    if incoming_msg == "clear":
        data.clear()
        data.append({"role": "assistant", "content": 'hello'})
    else:
        data.append({"role": "assistant", "content": incoming_msg})

    messages = [systemPrompt]
    messages.extend(data)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        content = response["choices"][0]["message"]["content"]
        return content
    except openai.error.RateLimitError as e:
        print(e)
        return ""


def get_dalle(incoming_msg):
    try:
        response = openai.Image.create(
            prompt=incoming_msg, n=1, size="512x512"
        )
        content = response['data'][0]['url']
        return content
    except openai.error.RateLimitError as e:
        print(e)
        return ""


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/chatgpt/")
@login_required
def chatgpt():
    """List members."""
    return render_template("users/chatgpt.html")


# Define route for home page
@blueprint.route("/gpt_endpoint", methods=["GET", "POST"])
@login_required
def gpt_endpoint():
    userText = request.args.get('msg')
    return str(get_gpt(userText))
