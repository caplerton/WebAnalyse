import os
import random

from plot_page.control.base_functions import write_json


def generate_data(id: int, **kwargs) -> dict:
    """Generate a random dict.

    Args:
        id (int): Id of the datapoint.

    Returns:
        dict: The created random dictionary.
    """
    result = {"id": id}
    for key, value in kwargs.items():
        if  value.get("type", None) == "float":
            result[key] = random.uniform(value.get("start", 0), value.get("end", 1))
        if value.get("type", None) == "int":
            result[key] = random.randint(value.get("start", 0), value.get("end", 1))
        if "options" in value:
            result[key] = random.choice(value["options"])
    return result

def generate_testdata( number_elements: int ,**kwargs) -> list[dict]:
    """Function to generate a list of random data.

    Args:
        number_elements (int): Number of elements that should be created.

    Returns:
        list[dict]: The created random dataset.
    """
    return [generate_data( i, **kwargs) for i in range(number_elements)]


test = generate_testdata(4000, type={"options": ["BMW", "VW", "Audi"]}, iteration={"type":"int", "start": 0, "end": 30}, ps={"type": "int", "start": 50, "end": 150}, km={"type": "float", "start": 0, "end": 200000}, backlights= {"type": "int"}, wheels={"type": "int"})
write_json(os.path.join(".", "test2.json"), {"input2": test})