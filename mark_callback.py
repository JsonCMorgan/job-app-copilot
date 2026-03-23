import os

from user_utils import get_user_paths

def main():
    _, outputs_dir = get_user_paths()
    output_files = [f for f in os.listdir(outputs_dir) if f.endswith(".txt")]
    if not output_files:
        print("No application files found in your outputs.")
        return
    for i, filename in enumerate(output_files, 1):
        print(f"{i}. {filename}")
    while True:
        choice = input("Enter the number of the application to mark as callback: ")
        try:
            index = int(choice) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if index < 0 or index >= len(output_files):
            print("Choice out of range. Please enter a valid number.")
            continue
        break
    chosen_filename = output_files[index]
    path = os.path.join(outputs_dir, chosen_filename)
    with open(path, "r") as f:
        content = f.read()
    content = content.replace("Callback: No", "Callback: Yes")
    with open(path, "w") as f:
        f.write(content)
    print(f"Marked {chosen_filename} as callback.")


if __name__ == "__main__":
    main()
