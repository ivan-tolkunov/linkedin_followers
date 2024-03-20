# LinkedIn Info

This Flask project allows you to parse LinkedIn followers and retrieve their profile photos as JSON data.

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.x
- Flask
- LinkedIn login and password

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ivan-tolkunov/linkedin_info.git
   ```

2. Navigate to the project directory:

   ```bash
   cd linkedin_info
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your LinkedIn API credentials:

   - Create a LinkedIn Developer account and create a new application.
   - Obtain the client ID and secret.
   - Update the `config.py` file with your credentials.

## Usage

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000/get_linkedin_info?linkedin_url=https://www.linkedin.com/in/user/`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
