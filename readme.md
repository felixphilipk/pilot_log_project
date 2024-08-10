#  PilotLog Project

This project is a Django-based application designed to manage Pilot Logs. It includes features for importing and exporting log data, with a focus on integration with Spark for data transformation.

**Install the Required Packages:**

pip install -r requirements.txt


### Running the Project

 **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

**Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

 **Access the Application:**

   Open your browser and navigate to `http://127.0.0.1:8000/` to access the application.

### Importing Data

To import data, use the import endpoint provided in the `urls.py`:

```plaintext
http://127.0.0.1:8000/import/
```

- Upload your JSON data to be processed by the Spark transformer and stored in the Django models.

### Exporting Data

To export data, use the export endpoint:

```plaintext
http://127.0.0.1:8000/export/
```

- This will trigger a CSV file download of the processed log data.

### CSRF Token

To retrieve the CSRF token for any POST requests:

```plaintext
http://127.0.0.1:8000/csrf-token/
```
