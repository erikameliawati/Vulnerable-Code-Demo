import sqlite3
import os


# Initialize database
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT, email TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', 'secret123', 'admin@company.com')")
    cursor.execute("INSERT INTO users VALUES ('user', 'pass456', 'user@company.com')")
    cursor.execute("INSERT INTO users VALUES ('alice', 'mypassword', 'alice@company.com')")
    return conn


def login_vulnerable(conn, username, password):
    """VULNERABLE: SQL Injection possible"""
    cursor = conn.cursor()

    # VULNERABLE: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    try:
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            print(f"Login successful! Welcome {result[0]}")
            print(f"Email: {result[2]}")
        else:
            print("Login failed!")
    except Exception as e:
        print(f"Error: {e}")


def execute_system_command(filename):
    """VULNERABLE: Command Injection through unsanitized input"""
    print(f"\n[Executing]: Listing details for {filename}")

    # VULNERABLE: User input directly in system command
    # Windows uses 'dir', Linux/Mac uses 'ls -la'
    if os.name == 'nt':  # Windows
        command = f"dir {filename}"
    else:  # Linux/Mac
        command = f"ls -la {filename}"

    print(f"[Running command]: {command}")
    os.system(command)


def sql_injection_demo():
    print("\n" + "=" * 70)
    print("VULNERABILITY 1: SQL INJECTION (VULNERABLE VERSION)")
    print("=" * 70)
    print("\nAvailable users: admin/secret123, user/pass456, alice/mypassword")

    conn = init_db()

    while True:
        print("\n--- SQL Injection Test ---")
        username = input("Enter username (or 'q' to quit): ").strip()
        if username.lower() == 'q':
            break

        password = input("Enter password: ").strip()
        login_vulnerable(conn, username, password)

    conn.close()


def command_injection_demo():
    print("\n" + "=" * 70)
    print("VULNERABILITY 2: COMMAND INJECTION (VULNERABLE VERSION)")
    print("=" * 70)
    print("\nThis simulates a file information tool.")

    # Create test files
    with open("document.txt", "w") as f:
        f.write("This is a test document.")
    with open("report.txt", "w") as f:
        f.write("This is a test report.")

    print("\nTest files created: document.txt, report.txt")
    print("\n Try these command injection attacks:")

    while True:
        print("\n--- File Info Tool ---")
        filename = input("Enter filename to check (or 'q' to quit): ").strip()
        if filename.lower() == 'q':
            break

        execute_system_command(filename)


def main():
    print("=" * 70)
    print("VULNERABLE CODE DEMO")
    print("=" * 70)
    print("\nThis demonstrates common security vulnerabilities.")

    while True:
        print("\n--- Main Menu ---")
        print("1. SQL Injection Demo")
        print("2. Command Injection Demo")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            sql_injection_demo()
        elif choice == '2':
            command_injection_demo()
        elif choice == '3':
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
