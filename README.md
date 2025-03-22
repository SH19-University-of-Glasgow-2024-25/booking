# SH19 Booking Platform

## Developers
- Aiden Lindsay - 2747612l@student.gla.ac.uk
- Josh Adams - 2765024a@student.gla.ac.uk
- Paul McHugh - 2775943m@student.gla.ac.uk
- Bobby Stone - 2773410s@student.gla.ac.uk
- Liam Murphy - 2759113m@student.gla.ac.uk
- Usmaan Wahab - 2777904w@student.gla.ac.uk
- Peter Warrington - 2746910w@student.gla.ac.uk

## Overview
A booking platform developed as part of a year-long team project at the University of Glasgow. This project is built using React, Django, and PostgreSQL. To learn more about the project read the frontend and backend developer guides and the user guide.

Below is a guide of some of the system, further guides are found in the front and backend READMEs and in the docs folder.

# Docker

## Initial Setup
This project is run through docker. Please install the docker engine and docker compose. The simplest way of achieving this is by installing [docker desktop](https://www.docker.com/products/docker-desktop/). Once installed you may be prompted to restart your device (which you should do even if it doesn't prompt you to). Once docker desktop is correctly installed and running your will need to obtain the `.env.dev` file which contains sensitive information that is required to run our application and place this file in the root `sh19-main`. Then run `docker compose --env-file .env.dev -f docker-compose-dev.yml up`. This will pull the images and begin configuration, please do not interupt this. Once this command is run there should be no new text appearing on the terminal. On the first run of this Django will complain and cause errors, this is because the database has yet to actually be created. To resolve this stop the current services using `Ctrl+c` and it will begin stopping the containers. Then again run `docker compose --env-file .env.dev -f docker-compose-dev.yml up`. The docker compose command is how you will run and view changes you've made to the software.

Note: you may need to add your user to the docker group if you get a permissions error, follow this [guide](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

Use `docker ps --format "{{.Names}}"` to view the names of running containers.

## Debugging PostgreSQL
If you would like to view the database directly, use the following sequence of comamnds.
- `(sudo) docker compose --env-file .env.dev -f docker-compose-dev.yml up`
    - Build/run the containers like normal.
- In a new terminal session: `docker exec -it <container_name> bash`
    - This will open a bash session within the docker container for the database.
- `psql -U bookingandbilling_webapp -d bookingandbilling`
    - This will connect you to the `bookingandbilling` database as the `bookingandbilling_webapp` user.

## Debugging Django or React
Live bash shell does not work on the `sh19-main-django-1` nor the `sh19-main-react-1` containers.
Instead you will have to run commands directly onto the container using the following.
- `(sudo) docker compose --env-file .env.dev -f docker-compose-dev.yml up`
    - Build/run the containers like normal.
- `(sudo) docker exec -it <container_name> <command>`
    - For example,
        - `docker exec -it sh19-main python3 manage.py makemigrations`
        - `docker exec -it sh19-main ls`
    - Remember you can run multiple commands consecutively using `<command_one> && <command_two> && ...`

# API Guide

All API responses follow a set format so that errors can easily be detected and error information displayed. `bookingandbilling.utilities` provides `APIresponse` and `ErrorResponse` classes that inherit from and replace the use of the standard REST framework `Response` class to enforce this format.

## API Response Format

```
{
   "status": "error" / "success",
IF NOT ERROR:
   "result": { ... Normal response data...},
ELSE IF ERROR:
    "error": {
        "error-code": "some-error-code"
        "error-http-code": 400 etc,
        "error-message": "User friendly error message",
        "error-data": { ... optional additional error data for use by the frontend ...}
        "error-list": ["optional list of", "errors", "for example for errors returned", "by a serialiser"]
    }
}
```

## Usage
### Backend

#### Imports:
```python
from .utilities import (
    APIresponse,
    APIerror,
    ErrorResponse,
    INTERNAL_ERROR_RESPONSE
)
```

#### To return a response without errors:

```python
return APIresponse(
        { ... normal response data ...},
        status.HTTP_XXX_CODE
    )
```

Example:

```python
return APIresponse(
        {
            "user": serializer.data,
            "token": token.key
        },
        status.HTTP_201_CREATED
    )
```

#### To return a response with a single error:

```python
return ErrorResponse(
    APIerror("error-code", 
                status.HTTP_XXX_CODE, 
                "Short error message")
    )
```

#### To return a response with multiple errors:

```python
return ErrorResponse(
    APIerror("error-code", 
                status.HTTP_XXX_CODE, 
                "Short error message",
                error_list=["List of", "Errors", "!"])
    )
```

#### To return optional custom data:

```python
return ErrorResponse(
    APIerror("error-code", 
                status.HTTP_XXX_CODE, 
                "Short error message",
                error_data={ ... some custom data that may be used by frontend ... })
    )
```

#### To return an unknown error:

```python
return INTERNAL_ERROR_RESPONSE
```

Which is defined in utilities.py:

```python
INTERNAL_ERROR_RESPONSE = ErrorResponse(
    APIerror(
        "django-error", 
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        "Unknown Django error"
           )
           )
```

### Frontend:

In order to communicate with backend...

Import the API client and error display function:

```ts
import {GenerateErrorDisplayElement} from "./utilities/Error";
import apiClient from './utilities/apiClient';
```

Set up an error element for displaying errors:

```ts
const [errorElm, setErrorElm] = useState(<div></div>);
```

Place that element in some visible place in your HTML, for example:
```html
...
    <button type="submit">Log In</button>
    {errorElm}
</form>
...
```

Make your requests in the following way:
```ts
apiClient.get("/whatever-endpoint")
    .then((res) => {
        if (res.data.status == "success") {
            // Do stuff with res.data.result!!
        } else if (res.data.status == "error") {
            setErrorElm(GenerateErrorDisplayElement(res.data.error));
        }
    })
    .catch((err) => {
        setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
    });
```



# Authentication

## Overview
Django Rest Framework (DRF) has been setup to use token authentication. By default API views will require a user to be logged in to access them. When a user logs in, a token is generated and stored for the account being accessed. This token is both stored on the backend and provided to the client. The token provided to the client is stored in a HTTP-Only cookie. This cookie exists for 1 day, and persists between sessions. This cookie is automatically attached to all API calls made using the axios apiClient. The cookie is HTTP-Only, therefore it cannot be accessed directly in JavaScript (protecting the authToken from XSS attacks). When a user logs out, the cookie holding the token is deleted, and the token is deleted from the backend. The default DRF token authentication method requires the authToken to be attached to requests as a header, not as a cookie - therefore the method has been overridden in `backend/bookingandbilling/middleware.py` and referrenced in `settings.py`.

## How To...

### Call an API Endpoint
In `frontend/src/utilities/apiClient.tsx` an instance of axios (an API client) is created with our required settings. All API calls should be made using this instance. This can be accessed on a page similarly to (if not exactly like) this `import apiClient from './utilities/apiClient';`.

An API endpoint will need to have been made as desired and included in `backend/bookingandbilling/urls.py`. This can then be called as follows: `apiClient.post("/register/", returnData)`, where `post` can be replaced by `get`, `/register/` can be replaced by any endpoint url, and `returnData` is a dictionary containing the required post values (or be ommitted entirely if not needed - ie get).

### Make API Endpoints Require / Not Require Login
All API Endpoints require the request to contain a valid authToken by default - which is automatically handled by the API client if it exists. To allow access to non authenticated users / calls put `permission_classes = [AllowAny]` at the top of the endpoint.

### Check the User Type calling an Endpoint
The request authToken can be got using `request.COOKIES.get('authToken')`. From this, the associated `User` model can be accessed using `get_user_from_token(token)` which returns None if token is None or an associated user is not found. The user returned is of the base `User` model. To retrieve the high-level user and learn it's type, you can use `user, type = get_full_user(user)` which returns the high-level user type (of type Admin, Interpreter or Customer) and the type as an AccountType ENUM value.

### Restrict an API to specific user types
There is a custom permission class that can be used to restrict APIs to specific user types. To use it include `permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN, AccountType.CUSTOMER])]` at the top of the endpoint - where the `allowed_types` list can contain any AccountType ENUM values. This will allow only users of a type listed to access the endpoint.

### Restrict Access to Pages
The `frontend/src/utilities/ProtectedRoute.tsx` component can be wrapped around other React components. It has three boolean properties which determine which user types can access the page. By default no account types are allowed so they must be specified. While this can be used anywhere, I do not see it being used outside of `App.tsx`. It is imported as `import ProtectedRoute from './utilities/ProtectedRoute';` and used as `<ProtectedRoute admin_access customer_access interpreter_access><PageToBeProtected /></ProtectedRoute>` where the `*_access` properties specify the allowed user types and the middle component is the protected content / page. Examples of this can be found in `App.tsx`. If a disallowed account type tries to access one of these pages they will be returned to the login page.

### Restrict Access to Specific Page Content
The `frontend/src/utilities/ProtectedComponent.tsx` component can be wrapped around other React components. It is imported as `import ProtectedComponent from './utilities/ProtectedComponent';` and used identically to the `ProtectedRoute` component described above. If a disallowed account type tries to load the page content nothing is rendered.

# Hosting

The application is currently hosted on AWS EC2, using the free tier.\
To access the EC2 instance you will need to securely provide @usmaan or someone else with your public ssh key.\
The following is an example for a block in your `.ssh/config` file.
```
Host aws
	HostName <EC2-ip>
	User ec2-user
```

You can then run `ssh aws`.

The EC2 instance uses the `docker-compose-prod.yml` which will be invoked using the following command,\
`sudo docker-compose --env-file .env.dev -f docker-compose-prod.yml up 2>&1 | tee output.log`.\
Conversely you would run `sudo docker-compose --env-file .env.dev -f docker-compose-prod.yml down` or forcefully using `docker stop $(docker ps -q)`

If you need to do anything related to git, this will take place over HTTPS rather than SSH as the ssh port for stgit is not available on external networks.
Which means you will need to put your GUID and password when using any git commands that require network operations.

If you need to make any changes please do them through GitLab and pull them, although an automatic CI production pipeline will be implemented soon.
Do **NOT** connect to AWS via vscode tunneling, as this seem to cause issues and makes the EC2 instance unresponsive. 
