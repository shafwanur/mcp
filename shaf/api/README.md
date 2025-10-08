## File Structure

* `models.py` holds all the **Pydantic models**. It defines the data shapes and validation rules, currently just for incoming requests.  

* `helpers.py` contains the core **business logic** for the API endpoints.

* `routes.py` defines all the **API endpoints** (routes). Handles incoming HTTP requests, calling the appropriate helper functions from `helpers.py`, and returning the final response. 