from src import create_app

# Start the app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
