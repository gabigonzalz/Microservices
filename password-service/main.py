from app import create_app

# Calls the create app function to start the password microservice
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
