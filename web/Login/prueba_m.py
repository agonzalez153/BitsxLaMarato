import sys
import time

try:
    from supabase import create_client, Client
except ImportError:
    print("Error: Supabase package not found. Please install it using:")
    print("pip install supabase")
    sys.exit(1)

# Supabase project URL and API key
SUPABASE_URL = "https://supdrzpdynaekvysaeio.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN1cGRyenBkeW5hZWt2eXNhZWlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQxODQzNjAsImV4cCI6MjA0OTc2MDM2MH0.PpDKwNEUt2l5h2rISdhjgjShzKijozx_dmnKoLFFSMM"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error connecting to Supabase: {str(e)}")
    sys.exit(1)

def create_account():
    try:
        print("\n=== Create Account ===")
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        if response.user:
            print("\nAccount created successfully!")
            print("Please check your email to verify your account.")
            time.sleep(2)
        else:
            print("\nError creating account")
    except Exception as e:
        print(f"\nError: {str(e)}")

def login():
    try:
        print("\n=== Login ===")
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        if response.session:
            print("\nLogged in successfully!")
            print(f"User UUID: {response.user.id}")
            time.sleep(2)
        else:
            print("\nError logging in")
    except Exception as e:
        if "Email not confirmed" in str(e):
            print("\nError: Please confirm your email address before logging in.")
            print("Check your inbox for the confirmation email.")
        else:
            print(f"\nError: {str(e)}")

def main():
    while True:
        print("\n=== Supabase Authentication ===")
        print("1. Create account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
    finally:
        input("\nPress Enter to exit...")
