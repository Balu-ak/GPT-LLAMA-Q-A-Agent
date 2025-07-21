{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "fe12c203-e6a6-452c-a655-afb8a03a4ff5",
   "metadata": {},
   "source": [
    "# GPT-LLAMA-Q&A-Agent\n",
    "\n",
    "To demonstrate your familiarity with OpenAI API, and also Ollama, build a tool that takes a technical question,  \n",
    "and responds with an explanation. This is a tool that you will be able to use yourself during the course!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "c1070317-3ed9-4659-abe3-828943230e03",
   "metadata": {},
   "outputs": [],
   "source": [
    "# imports\n",
    "import os\n",
    "import requests\n",
    "import json\n",
    "from typing import List\n",
    "from dotenv import load_dotenv\n",
    "from bs4 import BeautifulSoup\n",
    "from IPython.display import Markdown, display, update_display\n",
    "from openai import OpenAI"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "e7dbc4b2-fde1-4026-993f-342110e9340d",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "python(35151) MallocStackLogging: can't turn off malloc stack logging because it was not enabled.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[?2026h\u001b[?25l\u001b[1Gpulling manifest ⠋ \u001b[K\u001b[?25h\u001b[?2026l\u001b[?2026h\u001b[?25l\u001b[1Gpulling manifest ⠙ \u001b[K\u001b[?25h\u001b[?2026l\u001b[?2026h\u001b[?25l\u001b[1Gpulling manifest ⠹ \u001b[K\u001b[?25h\u001b[?2026l\u001b[?2026h\u001b[?25l\u001b[1Gpulling manifest ⠸ \u001b[K\u001b[?25h\u001b[?2026l\u001b[?2026h\u001b[?25l\u001b[1Gpulling manifest ⠼ \u001b[K\u001b[?25h\u001b[?2026l\u001b[?2026h\u001b[?25l\u001b[1Gpulling manifest \u001b[K\n",
      "pulling dde5aa3fc5ff: 100% ▕██████████████████▏ 2.0 GB                         \u001b[K\n",
      "pulling 966de95ca8a6: 100% ▕██████████████████▏ 1.4 KB                         \u001b[K\n",
      "pulling fcc5a6bec9da: 100% ▕██████████████████▏ 7.7 KB                         \u001b[K\n",
      "pulling a70ff7e570d9: 100% ▕██████████████████▏ 6.0 KB                         \u001b[K\n",
      "pulling 56bb8bd477a5: 100% ▕██████████████████▏   96 B                         \u001b[K\n",
      "pulling 34bb5ab01051: 100% ▕██████████████████▏  561 B                         \u001b[K\n",
      "verifying sha256 digest \u001b[K\n",
      "writing manifest \u001b[K\n",
      "success \u001b[K\u001b[?25h\u001b[?2026l\n"
     ]
    }
   ],
   "source": [
    "!ollama pull llama3.2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "4a456906-915a-4bfd-bb9d-57e505c5093f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# constants\n",
    "\n",
    "MODEL_GPT = 'gpt-4o-mini'\n",
    "MODEL_LLAMA = 'llama3.2'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "a8d7923c-5f28-4c30-8556-342d7c8497c1",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "API key found and looks good so far!\n"
     ]
    }
   ],
   "source": [
    "# set up environment\n",
    "load_dotenv(override=True)\n",
    "api_key = os.getenv('OPENAI_API_KEY')\n",
    "\n",
    "# Check the key\n",
    "\n",
    "if not api_key:\n",
    "    print(\"No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!\")\n",
    "elif not api_key.startswith(\"sk-proj-\"):\n",
    "    print(\"An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook\")\n",
    "elif api_key.strip() != api_key:\n",
    "    print(\"An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook\")\n",
    "else:\n",
    "    print(\"API key found and looks good so far!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "0ac6b6ef-9ce7-4dd1-999c-a88b6972cee7",
   "metadata": {},
   "outputs": [],
   "source": [
    "openai = OpenAI()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "3f0d0137-52b0-47a8-81a8-11a90a010798",
   "metadata": {},
   "outputs": [],
   "source": [
    "# here is the question; type over this to ask something new\n",
    "\n",
    "question = \"\"\"\n",
    "Please explain what this code does and why:\n",
    "yield from {book.get(\"author\") for book in books if book.get(\"author\")}\n",
    "\"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "60ce7000-a4a5-4cce-a261-e75ef45063b4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Answer from GPT-4o-mini:\n",
      "\n",
      "This line of code uses Python's generator expression to yield values from a set comprehension, specifically focusing on extracting the \"author\" key from a collection of `book` dictionaries. Let's break it down step by step:\n",
      "\n",
      "1. **Set Comprehension**: \n",
      "   The portion within the braces `{ ... }` is a set comprehension, which creates a set of unique values. It iterates over the `books` collection and collects authors from each book. \n",
      "\n",
      "   ```python\n",
      "   {book.get(\"author\") for book in books if book.get(\"author\")}\n",
      "   ```\n",
      "\n",
      "   - `for book in books`: This part iterates through each item in the `books` collection (which is assumed to be a list of dictionaries).\n",
      "   - `book.get(\"author\")`: Fetches the value associated with the \"author\" key from the `book` dictionary.\n",
      "   - `if book.get(\"author\")`: This condition filters out any books where the \"author\" key is either missing or evaluates to a falsy value (e.g., `None`, an empty string).\n",
      "\n",
      "   As a result, the set comprehension will create a set containing unique author names found in the `books` collection.\n",
      "\n",
      "2. **Yielding Values**:\n",
      "   The `yield from` statement is used to yield all values from an iterable. In this case, it yields each author from the set generated by the set comprehension.\n",
      "\n",
      "   ```python\n",
      "   yield from ...\n",
      "   ```\n",
      "\n",
      "   Here, `yield from` effectively loops over the set of authors and returns each author one at a time as the generator is iterated.\n",
      "\n",
      "### Summary:\n",
      "\n",
      "- **Purpose**: This code extracts unique authors from a list of `books`, where each book is a dictionary that may or may not contain an \"author\" key. It yields each unique author one at a time.\n",
      "  \n",
      "- **Why Use This Approach**: \n",
      "   - **Avoid Duplicates**: Using a set automatically removes duplicate author entries.\n",
      "   - **Efficiency**: It allows for efficient iteration over potentially large datasets by yielding items lazily, rather than constructing an entire list upfront.\n",
      "  \n",
      "In context, this line of code would typically be found within a generator function, allowing you to retrieve a series of unique authors on demand in a memory-efficient manner.None"
     ]
    }
   ],
   "source": [
    "# Get gpt-4o-mini to answer, with streaming\n",
    "response = openai.chat.completions.create(\n",
    "    model=\"gpt-4o-mini\",\n",
    "    messages=[{\"role\": \"user\", \"content\": question}],\n",
    "    stream=True\n",
    ")\n",
    "\n",
    "print(\"Answer from GPT-4o-mini:\\n\")\n",
    "for chunk in response:\n",
    "    delta = chunk.choices[0].delta\n",
    "    if hasattr(delta, \"content\"):\n",
    "        print(delta.content, end=\"\", flush=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "866fd2bd-b736-4f57-a2ff-e6850dab970c",
   "metadata": {},
   "outputs": [],
   "source": [
    "OLLAMA_API = \"http://localhost:11434/api/chat\"\n",
    "HEADERS = {\"Content-Type\": \"application/json\"}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "7a7b4afd-c7c7-4b95-87c6-775094ed6a24",
   "metadata": {},
   "outputs": [],
   "source": [
    "payload = {\n",
    "    \"model\": MODEL_LLAMA,\n",
    "    \"messages\": [\n",
    "        {\"role\": \"user\", \"content\": question}\n",
    "    ],\n",
    "    \"stream\": True\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "130b5a2a-5490-4116-96c2-5338fe078bf5",
   "metadata": {},
   "outputs": [],
   "source": [
    "response = requests.post(OLLAMA_API, json=payload, headers=HEADERS, stream=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "47f0ed93-a014-4f4e-8ea0-71df5ae14244",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Answer from LLaMA 3.2:\n",
      "\n",
      "This line of code is using a combination of generator expressions, dictionary methods, and the `yield from` syntax.\n",
      "\n",
      "Here's a breakdown:\n",
      "\n",
      "- `{...}`: This creates an expression that iterates over something (in this case, `books`). The results are collected into a new iterable.\n",
      "\n",
      "- `for book in books`: This part iterates over each item (`book`) in the `books` collection.\n",
      "\n",
      "- `.get(\"author\")`: For each item in the collection, this method retrieves the value associated with the key `\"author\"` from the dictionary-like object. If the key is not present or if the value cannot be converted to a string (for example, if the value is `None`), this method will return `None`.\n",
      "\n",
      "- `{...}`: Another iterable expression that collects the results of `.get(\"author\")` for each item in the collection.\n",
      "\n",
      "- `yield from {...}`: This syntax tells Python to use the iterable expression as an iterable and yields its values one at a time. It's similar to how `yield*` works, but it requires the input iterable to be a sequence (like a list or tuple), whereas `yield*` can work with any iterable.\n",
      "\n",
      "So, when you combine these elements, this line of code:\n",
      "\n",
      "- Iterates over each item in `books`.\n",
      "- For each item, tries to retrieve its `\"author\"` value from a dictionary-like object.\n",
      "- Yields the author's name if it exists; otherwise, yields `None`.\n",
      "\n",
      "This is likely used for some kind of data processing or filtering operation. It could be used to find all books by a specific author, filter out books without an author, etc.\n",
      "\n",
      "Here's an example:\n",
      "\n",
      "```python\n",
      "books = [\n",
      "    {\"title\": \"Book 1\", \"author\": \"Author A\"},\n",
      "    {\"title\": \"Book 2\", \"author\": None},\n",
      "    {\"title\": \"Book 3\", \"author\": \"Author B\"}\n",
      "]\n",
      "\n",
      "for author in yield from {book.get(\"author\") for book in books if book.get(\"author\")}:\n",
      "    print(author)\n",
      "```\n",
      "\n",
      "This will output:\n",
      "\n",
      "```\n",
      "Author A\n",
      "None\n",
      "Author B\n",
      "```"
     ]
    }
   ],
   "source": [
    "print(\"Answer from LLaMA 3.2:\\n\")\n",
    "for line in response.iter_lines():\n",
    "    if line:\n",
    "        try:\n",
    "            data = json.loads(line.decode(\"utf-8\"))\n",
    "            if \"message\" in data and \"content\" in data[\"message\"]:\n",
    "                print(data[\"message\"][\"content\"], end=\"\", flush=True)\n",
    "        except json.JSONDecodeError:\n",
    "            continue"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
