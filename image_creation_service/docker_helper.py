import docker
import time
import os

client = docker.from_env()
auth_config ={
    "username": "maheshbapatu",
    "password": "Nutanix.123"
}

def create_image(code, image_path):
    f = open(os.path.join(os.getcwd(), "server", "project", "main.py"), "w")
    f.write(code)
    f.close()
    image_name = "maheshbapatu/" + "areload" + str(int(time.time()))
    kwargs = {
        "path": os.path.join(os.getcwd(), "server"),
        "tag": image_name
    }
    print("Building Image")
    client.images.build(**kwargs)
    client.images.push(image_name, auth_config = auth_config)
    # os.system("docker save -o " + os.path.join(image_path, image_name) + " " + image_name)
    print("Image is built successfully")
    client.images.remove(image=image_name, force=True)
    return image_name
