import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def partial_search(search):
    search_results = []
    entries = list_entries()
    for search_element in entries:
        if search in search_element:
            search_results.append(search_element)
        else:
            pass
    if len(search_results) == 0:
        return None
    else:
        return search_results


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def random_result():
    return random.choice(list_entries())

def new_page(title, content):
    filename = f"entries/{title}.md"
    return default_storage.save(filename, ContentFile(content))
    #if default_storage.exists(filename):
    #    return None
    #else:
    #    return default_storage.save(filename, ContentFile(content))