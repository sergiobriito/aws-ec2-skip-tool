import tkinter as tk
from tkinter import messagebox
import boto3

def getClient(type):
    client = boto3.client(type)
    return client

def getInstanceIds(instanceNames, client):
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': instanceNames
            },
        ]
    )
    instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]
    return instance_ids

def setTagsOnInstance(instanceIds, tags, client):
    client.create_tags(
        Resources=instanceIds,
        Tags=tags
    )

def run():
    instanceNames = instanceNamesText.get("1.0", tk.END).strip().split('\n')
    if len(instanceNames) == 0:
        messagebox.showerror("Error", "Favor inserir os nomes das instancias")
        return

    tags = [
        {'Key': 'Skip', 'Value': skip_value.get()},
        {'Key': 'Skip_Until', 'Value': skip_until_value.get()}
    ]

    client = getClient("ec2")
    instance_ids = getInstanceIds(instanceNames, client)
    setTagsOnInstance(instance_ids, tags, client)
    messagebox.showinfo("Success", "Concluído!!!")

def main():
    global root, instanceNamesText, skip_value, skip_until_value

    root = tk.Tk()
    root.title("AWS EC2 Skip")

    tk.Label(root, text="Instance Names:").grid(row=0, column=0, padx=10, pady=5)
    instanceNamesText = tk.Text(root, height=10, width=50)
    instanceNamesText.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    tk.Label(root, text="Skip (True|False):").grid(row=2, column=0, padx=10, pady=5)
    skip_value = tk.Entry(root, width=50)
    skip_value.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Skip_Until (Date):").grid(row=3, column=0, padx=10, pady=5)
    skip_until_value = tk.Entry(root, width=50)
    skip_until_value.grid(row=3, column=1, padx=10, pady=5)

    execute_button = tk.Button(root, text="Execute", command=run)
    execute_button.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
